# Local DB Datasources — ObjectBox & Drift con TaskEither

Stack: `objectbox` · `objectbox_flutter_libs` · `drift` · `drift_flutter` · `fpdart`

---

## Tabla de contenidos

1. [Reglas generales para ambos motores](#reglas-generales-para-ambos-motores)
2. [ObjectBox](#objectbox) ← Setup del Store, datasource completo, queries, streams, transacciones
3. [Drift](#drift) ← Setup AppDatabase, datasource completo, upsert, streams, transacciones
4. [Consumir streams en Riverpod](#consumir-streams-reactivos-en-riverpod)
5. [Consumir streams en BLoC](#consumir-streams-reactivos-en-bloc)

---

## Reglas generales para ambos motores

- **Nunca lanzar** desde un datasource — siempre `TaskEither.tryCatch`.
- **Siempre envolver** el error nativo (`ObjectBoxException` / `DriftException`) antes de pasar a `ErrorHandler.map`.
- Las **migraciones** son operación crítica — usar `DbOperation.migration` y loguear siempre.
- Los **streams** (watchers) de ObjectBox y Drift deben convertirse a `Stream<Either<Failure, T>>`.

---

## ObjectBox

### Setup del Store (con manejo de error en inicialización)

```dart
// lib/core/local_db/objectbox_store.dart

import 'package:objectbox/objectbox.dart';
import 'package:path_provider/path_provider.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'objectbox.g.dart'; // generado por build_runner

part 'objectbox_store.g.dart';

@Riverpod(keepAlive: true)
Future<Store> objectBoxStore(ObjectBoxStoreRef ref) async {
  try {
    final dir = await getApplicationDocumentsDirectory();
    return openStore(directory: '${dir.path}/objectbox');
  } catch (e, st) {
    // Error fatal en apertura — registrar y re-lanzar para que Riverpod lo capture
    debugPrint('[ObjectBox] Error al abrir store: $e\n$st');
    rethrow;
  }
}
```

### Datasource completo con TaskEither

```dart
// features/products/data/datasources/products_objectbox_datasource.dart

import 'package:fpdart/fpdart.dart';
import 'package:objectbox/objectbox.dart';
import 'package:your_app/core/error/error_handler.dart';
import 'package:your_app/core/error/exceptions.dart';
import 'package:your_app/core/error/failures.dart';

class ProductsObjectBoxDatasource {
  const ProductsObjectBoxDatasource({required Store store})
      : _store = store;

  final Store _store;

  Box<ProductEntity> get _box => _store.box<ProductEntity>();

  // ─── Lectura ────────────────────────────────────────────────────────────────

  TaskEither<Failure, List<ProductEntity>> getAll() =>
      TaskEither.tryCatch(
        () async => _box.getAll(),
        (e, st) => _wrapObjectBox(e, st, DbOperation.read),
      );

  TaskEither<Failure, ProductEntity> getById(int id) =>
      TaskEither.tryCatch(
        () async {
          final entity = _box.get(id);
          if (entity == null) throw NotFoundException();
          return entity;
        },
        (e, st) => e is NotFoundException
            ? e as NotFoundException  // ya es AppException, ErrorHandler la mapea
            : _wrapObjectBox(e, st, DbOperation.read),
      ).flatMap((e) => TaskEither.of(e)); // propaga NotFoundException al ErrorHandler

  // ─── Escritura ──────────────────────────────────────────────────────────────

  TaskEither<Failure, int> save(ProductEntity entity) =>
      TaskEither.tryCatch(
        () async => _box.put(entity),
        (e, st) => _wrapObjectBox(e, st, DbOperation.write),
      );

  TaskEither<Failure, List<int>> saveAll(List<ProductEntity> entities) =>
      TaskEither.tryCatch(
        () async => _box.putMany(entities),
        (e, st) => _wrapObjectBox(e, st, DbOperation.write),
      );

  TaskEither<Failure, Unit> delete(int id) =>
      TaskEither.tryCatch(
        () async {
          _box.remove(id);
          return unit;
        },
        (e, st) => _wrapObjectBox(e, st, DbOperation.delete),
      );

  // ─── Queries ─────────────────────────────────────────────────────────────────

  TaskEither<Failure, List<ProductEntity>> findByCategory(String category) =>
      TaskEither.tryCatch(
        () async {
          final query = _box
              .query(ProductEntity_.category.equals(category))
              .order(ProductEntity_.name)
              .build();
          try {
            return query.find();
          } finally {
            query.close(); // SIEMPRE cerrar queries de ObjectBox
          }
        },
        (e, st) => _wrapObjectBox(e, st, DbOperation.query),
      );

  // ─── Streams (watchers) ──────────────────────────────────────────────────────

  /// Retorna Stream<Either<Failure, List<ProductEntity>>> para observar cambios.
  Stream<Either<Failure, List<ProductEntity>>> watchAll() {
    return _box
        .query()
        .watch(triggerImmediately: true)
        .map((query) {
          try {
            return Either<Failure, List<ProductEntity>>.right(query.find());
          } catch (e) {
            return Either.left(
              ErrorHandler.map(
                ObjectBoxException(cause: e, operation: DbOperation.read),
              ),
            );
          } finally {
            query.close();
          }
        });
  }

  // ─── Transacciones ──────────────────────────────────────────────────────────

  TaskEither<Failure, Unit> runTransaction(
    void Function(Box<ProductEntity> box) work,
  ) =>
      TaskEither.tryCatch(
        () async {
          _store.runInTransaction(TxMode.write, () => work(_box));
          return unit;
        },
        (e, st) => _wrapObjectBox(e, st, DbOperation.transaction),
      );

  // ─── Helper privado ──────────────────────────────────────────────────────────

  Failure _wrapObjectBox(Object e, StackTrace st, DbOperation op) =>
      ErrorHandler.map(
        ObjectBoxException(cause: e, operation: op),
        st,
      );
}
```

---

## Drift

### Setup de la base de datos

```dart
// lib/core/local_db/app_database.dart

import 'package:drift/drift.dart';
import 'package:drift_flutter/drift_flutter.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'app_database.g.dart'; // generado por build_runner

// Definición de tabla
class ProductsTable extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text().withLength(min: 1, max: 200)();
  TextColumn get category => text()();
  RealColumn get price => real()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [ProductsTable])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  @override
  MigrationStrategy get migration => MigrationStrategy(
    onCreate: (m) => m.createAll(),
    onUpgrade: (m, from, to) async {
      // Manejar migraciones futuras aquí
    },
  );
}

QueryExecutor _openConnection() => driftDatabase(name: 'app_database');

@Riverpod(keepAlive: true)
AppDatabase appDatabase(AppDatabaseRef ref) {
  final db = AppDatabase();
  ref.onDispose(db.close);
  return db;
}
```

### Datasource completo con TaskEither

```dart
// features/products/data/datasources/products_drift_datasource.dart

import 'package:drift/drift.dart';
import 'package:fpdart/fpdart.dart';
import 'package:your_app/core/error/error_handler.dart';
import 'package:your_app/core/error/exceptions.dart';
import 'package:your_app/core/error/failures.dart';
import 'package:your_app/core/local_db/app_database.dart';

class ProductsDriftDatasource {
  const ProductsDriftDatasource({required AppDatabase db}) : _db = db;

  final AppDatabase _db;

  // ─── Lectura ────────────────────────────────────────────────────────────────

  TaskEither<Failure, List<ProductsTableData>> getAll() =>
      TaskEither.tryCatch(
        () => _db.select(_db.productsTable).get(),
        (e, st) => _wrapDrift(e, st, DbOperation.read),
      );

  TaskEither<Failure, ProductsTableData> getById(int id) =>
      TaskEither.tryCatch(
        () async {
          final result = await (_db.select(_db.productsTable)
                ..where((t) => t.id.equals(id)))
              .getSingleOrNull();
          if (result == null) throw NotFoundException();
          return result;
        },
        (e, st) => e is NotFoundException
            ? ErrorHandler.map(e, st)
            : _wrapDrift(e, st, DbOperation.read),
      );

  TaskEither<Failure, List<ProductsTableData>> getByCategory(
      String category) =>
      TaskEither.tryCatch(
        () => (_db.select(_db.productsTable)
              ..where((t) => t.category.equals(category))
              ..orderBy([(t) => OrderingTerm.asc(t.name)]))
            .get(),
        (e, st) => _wrapDrift(e, st, DbOperation.query),
      );

  // ─── Escritura ──────────────────────────────────────────────────────────────

  TaskEither<Failure, int> insert(ProductsTableCompanion companion) =>
      TaskEither.tryCatch(
        () => _db.into(_db.productsTable).insert(companion),
        (e, st) => _wrapDrift(e, st, DbOperation.write),
      );

  TaskEither<Failure, bool> update(ProductsTableCompanion companion) =>
      TaskEither.tryCatch(
        () => _db.update(_db.productsTable).replace(companion),
        (e, st) => _wrapDrift(e, st, DbOperation.write),
      );

  /// Upsert — inserta o actualiza si ya existe
  TaskEither<Failure, int> upsert(ProductsTableCompanion companion) =>
      TaskEither.tryCatch(
        () => _db
            .into(_db.productsTable)
            .insertOnConflictUpdate(companion),
        (e, st) => _wrapDrift(e, st, DbOperation.write),
      );

  TaskEither<Failure, int> delete(int id) =>
      TaskEither.tryCatch(
        () => (_db.delete(_db.productsTable)
              ..where((t) => t.id.equals(id)))
            .go(),
        (e, st) => _wrapDrift(e, st, DbOperation.delete),
      );

  // ─── Streams (watch) ─────────────────────────────────────────────────────────

  /// Stream reactivo — se actualiza automáticamente con cada cambio en la tabla.
  Stream<Either<Failure, List<ProductsTableData>>> watchAll() {
    return (_db.select(_db.productsTable)
          ..orderBy([(t) => OrderingTerm.asc(t.name)]))
        .watch()
        .map(Either<Failure, List<ProductsTableData>>.right)
        .handleError(
          (e, st) => Either<Failure, List<ProductsTableData>>.left(
            _wrapDrift(e, st, DbOperation.read),
          ),
        );
  }

  // ─── Transacciones ──────────────────────────────────────────────────────────

  /// Drift maneja transacciones con `transaction()` que hace rollback automático
  /// si el Future lanza. Envolvemos para capturar y mapear el error.
  TaskEither<Failure, Unit> insertBatch(
    List<ProductsTableCompanion> companions,
  ) =>
      TaskEither.tryCatch(
        () async {
          await _db.transaction(() async {
            for (final c in companions) {
              await _db.into(_db.productsTable).insert(c);
            }
          });
          return unit;
        },
        (e, st) => _wrapDrift(e, st, DbOperation.transaction),
      );

  // ─── Helper privado ──────────────────────────────────────────────────────────

  Failure _wrapDrift(Object e, StackTrace st, DbOperation op) {
    // Intentar extraer el código SQLite de SqlException de Drift
    final sqliteCode = e is DriftWrappedException ? e.cause.hashCode : null;
    return ErrorHandler.map(
      DriftException(cause: e, operation: op, sqliteCode: sqliteCode),
      st,
    );
  }
}
```

---

## Consumir streams reactivos en Riverpod

```dart
// Proveedor que expone el stream como AsyncValue
@riverpod
Stream<Either<Failure, List<Product>>> productsStream(
  ProductsStreamRef ref,
) {
  final datasource = ref.watch(productsDriftDatasourceProvider);
  return datasource
      .watchAll()
      .map((either) => either.map(
            (rows) => rows.map(ProductMapper.fromDrift).toList(),
          ));
}

// Widget
ref.watch(productsStreamProvider).when(
  loading: () => const CircularProgressIndicator(),
  error: (e, _) => const UnexpectedErrorWidget(),
  data: (either) => either.fold(
    (failure) => FailureView(failure: failure),
    (products) => ProductsListView(products: products),
  ),
);
```

## Consumir streams reactivos en BLoC

```dart
// En el BLoC, suscribirse al stream en el constructor
ProductsBloc({required ProductsDriftDatasource datasource})
    : _datasource = datasource,
      super(const ProductsState.initial()) {
  on<ProductsWatchStarted>(_onWatchStarted);
}

Future<void> _onWatchStarted(
  ProductsWatchStarted event,
  Emitter<ProductsState> emit,
) async {
  await emit.onEach<Either<Failure, List<ProductsTableData>>>(
    _datasource.watchAll(),
    onData: (either) => either.fold(
      (f) => emit(ProductsState.failure(f)),
      (rows) => emit(ProductsState.loaded(
        rows.map(ProductMapper.fromDrift).toList(),
      )),
    ),
    onError: (e, _) => emit(
      ProductsState.failure(const UnexpectedFailure()),
    ),
  );
}
```
