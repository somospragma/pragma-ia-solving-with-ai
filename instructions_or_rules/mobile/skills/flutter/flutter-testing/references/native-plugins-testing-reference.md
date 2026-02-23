# Testing Native Plugins & Platform Dependencies Reference

Guía para testear código que depende de dispositivos nativos, plugins y canales de plataforma (iOS/Android).

## Desafíos de Testing de Plugins Nativos

| Desafío | Solución |
|---|---|
| No se ejecutan en Unit Tests | Usar mocks y fakes |
| Comportamiento específico de plataforma | Aislar lógica en interfaces |
| Acceso a hardware real | Usar platform channels | 
| Cambios de estado del dispositivo | Simular eventos |

## Arquitectura Recomendada

```dart
lib/
├── data/
│   ├── datasources/
│   │   ├── location_datasource.dart  // Interfaz
│   │   └── location_datasource_impl.dart  // Con plugin
│   └── repositories/
├── domain/
│   └── repositories/
│       └── location_repository.dart  // Interfaz
└── presentation/

test/
├── data/
│   ├── datasources/
│   │   └── location_datasource_test.dart
│   └── repositories/
│       └── location_repository_test.dart
└── fixtures/
    └── location_fake.dart
```

## Patrón: Aislar Dependencias Nativas

### 1. Crear Interfaz (No Depender del Plugin Directamente)

```dart
// lib/data/datasources/location_datasource.dart
abstract class LocationDataSource {
  Future<LocationData> getCurrentLocation();
  Stream<LocationData> watchLocation();
  Future<bool> requestPermission();
}

// Datos que retorna
class LocationData {
  final double latitude;
  final double longitude;
  final double altitude;
  final double accuracy;

  LocationData({
    required this.latitude,
    required this.longitude,
    required this.altitude,
    required this.accuracy,
  });
}

// Excepciones específicas
class LocationException implements Exception {
  final String message;
  LocationException(this.message);
}

class PermissionDeniedException extends LocationException {
  PermissionDeniedException() : super('Location permission denied');
}

class LocationUnavailableException extends LocationException {
  LocationUnavailableException() : super('Location service unavailable');
}
```

### 2. Implementación con Plugin Real

```dart
// lib/data/datasources/location_datasource_impl.dart
import 'package:geolocator/geolocator.dart';

class LocationDataSourceImpl implements LocationDataSource {
  final Geolocator _geolocator;

  LocationDataSourceImpl({
    Geolocator? geolocator,
  }) : _geolocator = geolocator ?? Geolocator();

  @override
  Future<LocationData> getCurrentLocation() async {
    try {
      // Verificar permisos
      final permission = await _checkPermission();
      if (!permission) {
        throw PermissionDeniedException();
      }

      // Verificar que el servicio está habilitado
      final isLocationServiceEnabled = 
          await _geolocator.isLocationServiceEnabled();
      if (!isLocationServiceEnabled) {
        throw LocationUnavailableException();
      }

      // Obtener ubicación
      final position = await _geolocator.getCurrentPosition(
        timeLimit: const Duration(seconds: 10),
        forceAndroidLocationManager: true,
      );

      return LocationData(
        latitude: position.latitude,
        longitude: position.longitude,
        altitude: position.altitude,
        accuracy: position.accuracy,
      );
    } on LocationException {
      rethrow;
    } catch (e) {
      throw LocationException('Failed to get location: $e');
    }
  }

  @override
  Stream<LocationData> watchLocation() {
    return _geolocator.getPositionStream().map(
      (position) => LocationData(
        latitude: position.latitude,
        longitude: position.longitude,
        altitude: position.altitude,
        accuracy: position.accuracy,
      ),
    ).handleError((error) {
      throw LocationException('Location stream error: $error');
    });
  }
}
```

## MethodChannel Testing: HTTP Request Pattern

**Oficial**: MethodChannel es async bridge entre Dart ↔ Native (iOS/Android/Windows).

### Patrón Real: HTTP Request a Través de MethodChannel

**lib/services/http_service.dart**:
```dart
import 'package:flutter/services.dart';

class HttpService {
  static const channel = MethodChannel('com.example.app/http');

  static Future<String> fetchData(String url) async {
    try {
      final result = await channel.invokeMethod<String>(
        'fetchUrl',
        {'url': url},
      );
      return result ?? 'Empty response';
    } on PlatformException catch (e) {
      throw HttpException('Native HTTP failed: ${e.message}');
    }
  }
}
```

### Test: Mockeando MethodChannel

**test/services/http_service_test.dart**:
```dart
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:myapp/services/http_service.dart';

void main() {
  const channel = MethodChannel('com.example.app/http');
  
  setUp(() {
    TestWidgetsFlutterBinding.ensureInitialized();
  });

  test('fetchData returns response on success', () async {
    // Arrange: Simular respuesta nativa
    channel.setMockMethodCallHandler((MethodCall methodCall) async {
      if (methodCall.method == 'fetchUrl') {
        return '{"status": "ok", "data": "Hello from Native"}';
      }
      return null;
    });

    // Act
    final result = await HttpService.fetchData('https://example.com/data');

    // Assert
    expect(result, contains('Hello from Native'));

    // Cleanup
    channel.setMockMethodCallHandler(null);
  });

  test('fetchData throws HttpException on error', () async {
    // Arrange: Simular error nativo
    channel.setMockMethodCallHandler((MethodCall methodCall) async {
      if (methodCall.method == 'fetchUrl') {
        throw PlatformException(
          code: 'NETWORK_ERROR',
          message: 'Connection failed',
        );
      }
      return null;
    });

    // Act & Assert
    expect(
      () => HttpService.fetchData('https://example.com/data'),
      throwsA(isA<HttpException>()),
    );

    channel.setMockMethodCallHandler(null);
  });

  test('fetchData passes correct URL to native', () async {
    final capturedUrl = <String>?[] as List<String?>;

    // Arrange
    channel.setMockMethodCallHandler((MethodCall methodCall) async {
      if (methodCall.method == 'fetchUrl') {
        capturedUrl.add(methodCall.arguments['url'] as String?);
        return '{"status": "ok"}';
      }
      return null;
    });

    // Act
    await HttpService.fetchData('https://api.example.com/users');

    // Assert
    expect(capturedUrl[0], equals('https://api.example.com/users'));

    channel.setMockMethodCallHandler(null);
  });
}
```

### Por Qué Este Patrón

- **Oficial**: Basado en docs.flutter.dev/platform-integration/platform-channels
- **Testeable**: Mock native sin compilar código Kotlin/Swift
- **Práctico**: HTTP es 80% del uso de MethodChannel
- **Completo**: Cubre success, error, y verificación de parámetros

### EventChannel (Streams desde Native)

Para datos en streaming (ubicación GPS, sensores):
```dart
// En Dart
final eventChannel = EventChannel('com.example.app/stream');

// En Test
eventChannel.receiveBroadcastStream().listen((event) {
  print('Event: $event');
});

// Mock similar a MethodChannel

  @override
  Future<bool> requestPermission() async {
    try {
      final permission = await _geolocator.requestPermission();
      return permission == LocationPermission.whileInUse ||
          permission == LocationPermission.always;
    } catch (e) {
      return false;
    }
  }

  Future<bool> _checkPermission() async {
    final permission = await _geolocator.checkPermission();
    return permission == LocationPermission.whileInUse ||
        permission == LocationPermission.always;
  }
}
```

### 3. Mock y Fake para Testing

```dart
// test/fixtures/location_fake.dart
class FakeLocationDataSource implements LocationDataSource {
  final _locationController = StreamController<LocationData>();

  final List<LocationData> locations = [];
  bool shouldThrowPermissionError = false;
  bool shouldThrowLocationError = false;

  @override
  Future<LocationData> getCurrentLocation() async {
    if (shouldThrowPermissionError) {
      throw PermissionDeniedException();
    }

    if (shouldThrowLocationError) {
      throw LocationUnavailableException();
    }

    if (locations.isEmpty) {
      return LocationData(
        latitude: 0.0,
        longitude: 0.0,
        altitude: 0.0,
        accuracy: 0.0,
      );
    }

    return locations.first;
  }

  @override
  Stream<LocationData> watchLocation() {
    return _locationController.stream;
  }

  @override
  Future<bool> requestPermission() async {
    if (shouldThrowPermissionError) {
      return false;
    }
    return true;
  }

  // Helpers para testing
  void emitLocation(LocationData location) {
    _locationController.add(location);
  }

  void simulateError(Exception error) {
    _locationController.addError(error);
  }

  void dispose() {
    _locationController.close();
  }
}

// test/fixtures/test_data.dart
const testLocation = LocationData(
  latitude: 40.7128,
  longitude: 74.0060,
  altitude: 10.0,
  accuracy: 5.0,
);

const testLocationAccurate = LocationData(
  latitude: 40.7128,
  longitude: 74.0060,
  altitude: 10.0,
  accuracy: 2.0,
);

const testLocationInaccurate = LocationData(
  latitude: 40.7128,
  longitude: 74.0060,
  altitude: 10.0,
  accuracy: 100.0,
);
```

## Testing de Casos Específicos de Plugins

### 1. Testing de Permisos

```dart
// test/data/datasources/location_datasource_test.dart
void main() {
  late FakeLocationDataSource fakeDataSource;

  setUp(() {
    fakeDataSource = FakeLocationDataSource();
  });

  tearDown(() {
    fakeDataSource.dispose();
  });

  group('LocationDataSource - Permissions', () {
    test('request permission returns true on success', () async {
      // Act
      final result = await fakeDataSource.requestPermission();

      // Assert
      expect(result, true);
    });

    test('request permission returns false on denial', () async {
      // Arrange
      fakeDataSource.shouldThrowPermissionError = true;

      // Act
      final result = await fakeDataSource.requestPermission();

      // Assert
      expect(result, false);
    });

    test('getCurrentLocation throws when permission denied', () async {
      // Arrange
      fakeDataSource.shouldThrowPermissionError = true;

      // Act & Assert
      expect(
        () => fakeDataSource.getCurrentLocation(),
        throwsA(isA<PermissionDeniedException>()),
      );
    });

    test('getCurrentLocation throws when service unavailable', () async {
      // Arrange
      fakeDataSource.shouldThrowLocationError = true;

      // Act & Assert
      expect(
        () => fakeDataSource.getCurrentLocation(),
        throwsA(isA<LocationUnavailableException>()),
      );
    });
  });
}
```

### 2. Testing de Streaming

```dart
group('LocationDataSource - Streaming', () {
  test('watchLocation emits location updates', () async {
    // Arrange
    fakeDataSource.emitLocation(testLocation);
    fakeDataSource.emitLocation(testLocationAccurate);

    // Act & Assert
    expect(
      fakeDataSource.watchLocation(),
      emitsInOrder([testLocation, testLocationAccurate]),
    );
  });

  test('watchLocation emits multiple locations sequentially', () async {
    // Arrange
    final locations = [testLocation, testLocationAccurate, testLocationInaccurate];

    // Act
    Future.delayed(Duration(milliseconds: 100), () {
      for (var loc in locations) {
        fakeDataSource.emitLocation(loc);
      }
    });

    // Assert
    expect(
      fakeDataSource.watchLocation(),
      emitsInOrder(locations),
    );
  });

  test('watchLocation handles errors', () async {
    // Arrange
    final error = LocationException('Connection lost');

    // Act
    Future.delayed(Duration(milliseconds: 50), () {
      fakeDataSource.simulateError(error);
    });

    // Assert
    expect(
      fakeDataSource.watchLocation(),
      emitsError(isA<LocationException>()),
    );
  });
});
```

### 3. Testing de Accuracy

```dart
group('LocationDataSource - Accuracy', () {
  test('getCurrentLocation returns accurate location', () async {
    // Arrange
    fakeDataSource.locations.add(testLocationAccurate);

    // Act
    final location = await fakeDataSource.getCurrentLocation();

    // Assert
    expect(location.accuracy, lessThan(5.0));
  });

  test('watchLocation filters inaccurate locations', () async {
    // Arrange
    // Crear wrapper que filtra
    final filteredStream = fakeDataSource.watchLocation()
        .where((location) => location.accuracy < 10.0);

    fakeDataSource.emitLocation(testLocationInaccurate);  // Será filtrado
    fakeDataSource.emitLocation(testLocationAccurate);    // Será emitido

    // Assert
    expect(
      filteredStream,
      emits(testLocationAccurate),
    );
  });
});
```

## Testing de Platform Channels

### 1. Mockear Method Channel

```dart
// lib/services/camera_service.dart
class CameraService {
  static const platform = MethodChannel('com.example.app/camera');

  Future<String> takePicture() async {
    try {
      final result = await platform.invokeMethod<String>('takePicture');
      return result ?? '';
    } on PlatformException catch (e) {
      throw CameraException('Failed to take picture: ${e.message}');
    }
  }

  Future<List<String>> getAvailableCameras() async {
    try {
      final result = await platform.invokeMethod<List<String>>('getAvailableCameras');
      return result ?? [];
    } on PlatformException catch (e) {
      throw CameraException('Failed to get cameras: ${e.message}');
    }
  }
}

// test/services/camera_service_test.dart
void main() {
  const channel = MethodChannel('com.example.app/camera');

  TestWidgetsFlutterBinding.ensureInitialized();

  tearDown(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, null);
  });

  group('CameraService', () {
    test('takePicture returns file path', () async {
      // Arrange
      final service = CameraService();
      
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
        switch (methodCall.method) {
          case 'takePicture':
            return '/storage/emulated/0/Pictures/photo.jpg';
          default:
            return null;
        }
      });

      // Act
      final result = await service.takePicture();

      // Assert
      expect(result, '/storage/emulated/0/Pictures/photo.jpg');
    });

    test('takePicture throws on platform error', () async {
      // Arrange
      final service = CameraService();
      
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
        throw PlatformException(
          code: 'CAMERA_ERROR',
          message: 'Camera not available',
        );
      });

      // Act & Assert
      expect(
        () => service.takePicture(),
        throwsA(isA<CameraException>()),
      );
    });

    test('getAvailableCameras returns list', () async {
      // Arrange
      final service = CameraService();
      
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
        switch (methodCall.method) {
          case 'getAvailableCameras':
            return ['0', '1'];  // Front y back
          default:
            return null;
        }
      });

      // Act
      final result = await service.getAvailableCameras();

      // Assert
      expect(result, ['0', '1']);
    });
  });
}
```

### 2. Testing de Event Channels

```dart
// lib/services/battery_service.dart
class BatteryService {
  static const batteryChannel = EventChannel('com.example.app/battery');

  Stream<int> getBatteryLevelStream() {
    return batteryChannel
        .receiveBroadcastStream()
        .map((event) => event as int)
        .handleError((error) {
          throw BatteryException('Battery service error: $error');
        });
  }
}

// test/services/battery_service_test.dart
void main() {
  const channel = EventChannel('com.example.app/battery');

  TestWidgetsFlutterBinding.ensureInitialized();

  group('BatteryService', () {
    test('getBatteryLevelStream emits battery levels', () async {
      // Arrange
      final service = BatteryService();
      
      TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
          .setMockMethodCallHandler(channel.binaryMessenger, (MethodCall methodCall) async {
        // Simular stream de eventos
        if (methodCall.method == 'listen') {
          // Enviar eventos simulados
          return null;
        }
        return null;
      });

      // Alternativa: Usar mockStub
      setMockMethodCallHandler(channel, (MethodCall methodCall) async {
        return Stream<int>.fromIterable([100, 80, 60, 40, 20]);
      });

      // Act & Assert
      expect(
        service.getBatteryLevelStream(),
        emitsInOrder([100, 80, 60, 40, 20]),
      );
    });
  });
}
```

## Testing de Plugins Comunes

### 1. Connectivity Plugin

```dart
// lib/services/connectivity_service.dart
abstract class ConnectivityService {
  Stream<ConnectivityStatus> watchConnectivity();
  Future<ConnectivityStatus> checkConnectivity();
}

enum ConnectivityStatus { online, offline, unknown }

class ConnectivityServiceImpl implements ConnectivityService {
  final Connectivity _connectivity;

  ConnectivityServiceImpl({Connectivity? connectivity})
      : _connectivity = connectivity ?? Connectivity();

  @override
  Stream<ConnectivityStatus> watchConnectivity() {
    return _connectivity.onConnectivityChanged.map(
      (result) => _mapToStatus(result),
    );
  }

  @override
  Future<ConnectivityStatus> checkConnectivity() async {
    final result = await _connectivity.checkConnectivity();
    return _mapToStatus(result);
  }

  ConnectivityStatus _mapToStatus(ConnectivityResult result) {
    switch (result) {
      case ConnectivityResult.mobile:
      case ConnectivityResult.wifi:
        return ConnectivityStatus.online;
      case ConnectivityResult.none:
        return ConnectivityStatus.offline;
      default:
        return ConnectivityStatus.unknown;
    }
  }
}

// test/fixtures/connectivity_fake.dart
class FakeConnectivityService implements ConnectivityService {
  final _controller = StreamController<ConnectivityStatus>();
  ConnectivityStatus _currentStatus = ConnectivityStatus.online;

  @override
  Stream<ConnectivityStatus> watchConnectivity() => _controller.stream;

  @override
  Future<ConnectivityStatus> checkConnectivity() async => _currentStatus;

  void simulateGoingOffline() {
    _currentStatus = ConnectivityStatus.offline;
    _controller.add(ConnectivityStatus.offline);
  }

  void simulateGoingOnline() {
    _currentStatus = ConnectivityStatus.online;
    _controller.add(ConnectivityStatus.online);
  }

  void dispose() => _controller.close();
}

// test/services/connectivity_service_test.dart
void main() {
  late FakeConnectivityService fakeService;

  setUp(() {
    fakeService = FakeConnectivityService();
  });

  tearDown(() {
    fakeService.dispose();
  });

  test('watchConnectivity emits status changes', () {
    expect(
      fakeService.watchConnectivity(),
      emitsInOrder([
        ConnectivityStatus.offline,
        ConnectivityStatus.online,
      ]),
    );

    fakeService.simulateGoingOffline();
    fakeService.simulateGoingOnline();
  });
}
```

### 2. SharedPreferences

```dart
// lib/services/local_storage_service.dart
abstract class LocalStorageService {
  Future<void> saveString(String key, String value);
  Future<String?> getString(String key);
  Future<void> clear();
}

class LocalStorageServiceImpl implements LocalStorageService {
  final SharedPreferences _prefs;

  LocalStorageServiceImpl(this._prefs);

  @override
  Future<void> saveString(String key, String value) async {
    await _prefs.setString(key, value);
  }

  @override
  Future<String?> getString(String key) async {
    return _prefs.getString(key);
  }

  @override
  Future<void> clear() async {
    await _prefs.clear();
  }
}

// test/fixtures/local_storage_fake.dart
class FakeLocalStorageService implements LocalStorageService {
  final Map<String, String> _storage = {};

  @override
  Future<void> saveString(String key, String value) async {
    _storage[key] = value;
  }

  @override
  Future<String?> getString(String key) async {
    return _storage[key];
  }

  @override
  Future<void> clear() async {
    _storage.clear();
  }
}

// test/services/local_storage_test.dart
void main() {
  late FakeLocalStorageService storage;

  setUp(() {
    storage = FakeLocalStorageService();
  });

  test('should save and retrieve string', () async {
    await storage.saveString('key', 'value');
    final result = await storage.getString('key');
    expect(result, 'value');
  });

  test('should return null for non-existent key', () async {
    final result = await storage.getString('nonexistent');
    expect(result, null);
  });

  test('should clear storage', () async {
    await storage.saveString('key1', 'value1');
    await storage.saveString('key2', 'value2');
    await storage.clear();

    expect(await storage.getString('key1'), null);
    expect(await storage.getString('key2'), null);
  });
}
```

## Mejores Prácticas

### ✅ Hacer

- Aislar plugins detrás de interfaces
- Crear fakes e implementaciones de test
- Testear manejo de errores de plataforma
- Simular diferentes estados del dispositivo
- Usar método channel mock en tests
- Documentar dependencias nativas

### ❌ Evitar

- Testear directamente con plugins
- Depender de hardware real en tests
- Ignorar plataformas específicas
- Hardcodear valores de estado
- Tests que requieren interacción manual

## Checklist de Testing de Plugins

- [ ] Interfaz creada sin dependencias de plugin
- [ ] Implementación real con plugin
- [ ] Fakes de test creados
- [ ] Permisos testados
- [ ] Errores de plataforma manejados
- [ ] Casos de éxito y error cubiertos
- [ ] Streaming testado si aplica
- [ ] Documentación de setup requerido
- [ ] Tests en CI/CD sin dispositivo real
