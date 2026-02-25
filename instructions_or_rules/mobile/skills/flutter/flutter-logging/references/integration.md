# Integración — Riverpod, BLoC, Datasources, Navegación

`AppLogger` se usa igual en todas las capas — siempre la misma fachada.

---

## Riverpod — logging desde AsyncNotifier

```dart
@riverpod
class CheckoutNotifier extends _$CheckoutNotifier {
  @override
  CheckoutState build() => const CheckoutState.initial();

  Future<void> submitOrder(Order order) async {
    state = const CheckoutState.loading();

    final stopwatch = Stopwatch()..start();

    final result = await ref.read(submitOrderUseCaseProvider).call(order).run();

    // Loguear latencia del usecase
    AppLogger.performance(
      'submit_order',
      durationMs: stopwatch.elapsedMilliseconds,
      context: {'order_id': order.id, 'amount': order.total},
    );

    state = result.fold(
      (failure) {
        // Loguear el error con contexto — fachada al skill de error handling
        AppLogger.error(
          'checkout_failed',
          error: failure,
          context: {'order_id': order.id, 'failure_type': failure.runtimeType.toString()},
        );
        return CheckoutState.failure(failure);
      },
      (confirmedOrder) {
        // Evento de negocio — va a DataDog y Grafana
        AppLogger.business(
          'purchase_completed',
          context: {'order_id': confirmedOrder.id, 'revenue': confirmedOrder.total},
        );
        return CheckoutState.success(confirmedOrder);
      },
    );
  }
}
```

---

## BLoC — logging desde event handlers

```dart
class OrdersBloc extends Bloc<OrdersEvent, OrdersState> {
  OrdersBloc({required GetOrdersUseCase getOrders})
      : _getOrders = getOrders,
        super(const OrdersState.initial()) {
    on<OrdersLoadRequested>(_onLoad);
  }

  final GetOrdersUseCase _getOrders;

  Future<void> _onLoad(
    OrdersLoadRequested event,
    Emitter<OrdersState> emit,
  ) async {
    emit(const OrdersState.loading());

    final stopwatch = Stopwatch()..start();
    final result = await _getOrders().run();
    final elapsed = stopwatch.elapsedMilliseconds;

    result.fold(
      (failure) {
        AppLogger.error(
          'orders_load_failed',
          error: failure,
          context: {'failure_type': failure.runtimeType.toString()},
        );
        emit(OrdersState.failure(failure));
      },
      (orders) {
        AppLogger.performance(
          'orders_loaded',
          durationMs: elapsed,
          context: {'count': orders.length},
        );
        emit(OrdersState.loaded(orders));
      },
    );
  }
}
```

---

## Datasources — logging de latencia de red

```dart
class ProductsRemoteDatasource {
  const ProductsRemoteDatasource({required Dio dio}) : _dio = dio;
  final Dio _dio;

  TaskEither<Failure, List<Product>> getProducts() =>
      TaskEither.tryCatch(
        () async {
          final stopwatch = Stopwatch()..start();

          final response = await _dio.get<List<dynamic>>('/products');

          // Loguear latencia de cada llamada de red
          AppLogger.performance(
            'api_request',
            durationMs: stopwatch.elapsedMilliseconds,
            context: {
              'endpoint': '/products',
              'status': response.statusCode,
              'count': response.data?.length ?? 0,
            },
          );

          return (response.data ?? [])
              .map((e) => ProductDto.fromJson(e as Map<String, dynamic>))
              .map((dto) => dto.toDomain())
              .toList();
        },
        (error, stackTrace) {
          AppLogger.error(
            'api_request_failed',
            error: error,
            stackTrace: stackTrace,
            context: {'endpoint': '/products'},
          );
          return ErrorHandler.map(error, stackTrace);
        },
      );
}
```

---

## Navegación — NavigatorObserver

Para loguear automáticamente todas las transiciones de pantalla sin añadir
`AppLogger.navigation()` manualmente en cada ruta:

```dart
// lib/core/logging/navigation_log_observer.dart

class NavigationLogObserver extends NavigatorObserver {
  @override
  void didPush(Route route, Route? previousRoute) {
    AppLogger.navigation(
      from: previousRoute?.settings.name ?? 'unknown',
      to: route.settings.name ?? 'unknown',
    );
  }

  @override
  void didPop(Route route, Route? previousRoute) {
    AppLogger.navigation(
      from: route.settings.name ?? 'unknown',
      to: previousRoute?.settings.name ?? 'unknown',
      context: {'action': 'pop'},
    );
  }

  @override
  void didReplace({Route? newRoute, Route? oldRoute}) {
    AppLogger.navigation(
      from: oldRoute?.settings.name ?? 'unknown',
      to: newRoute?.settings.name ?? 'unknown',
      context: {'action': 'replace'},
    );
  }
}

// Registro en MaterialApp o GoRouter:

// MaterialApp
MaterialApp(
  navigatorObservers: [NavigationLogObserver()],
  // ...
)

// GoRouter
GoRouter(
  observers: [NavigationLogObserver()],
  // ...
)
```

---

## BlocObserver — logging global de BLoC

```dart
// lib/core/observers/logging_bloc_observer.dart

class LoggingBlocObserver extends BlocObserver {
  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    super.onError(bloc, error, stackTrace);
    AppLogger.error(
      'bloc_unhandled_error',
      error: error,
      stackTrace: stackTrace,
      context: {'bloc': bloc.runtimeType.toString()},
    );
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    super.onTransition(bloc, transition);
    // Solo en debug para no saturar los handlers en prod
    AppLogger.debug(
      'bloc_transition',
      context: {
        'bloc': bloc.runtimeType.toString(),
        'event': transition.event.runtimeType.toString(),
        'next_state': transition.nextState.runtimeType.toString(),
      },
    );
  }
}

// En main():
// Bloc.observer = LoggingBlocObserver();
```
