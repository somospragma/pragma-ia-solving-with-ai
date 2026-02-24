# BLoC / Cubit Integration — Either + Failure

Stack: `flutter_bloc` · `fpdart` · Dart 3.3+

---

## Estado sellado con Failure

```dart
// features/products/presentation/bloc/products_state.dart

import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:your_app/core/error/failures.dart';

part 'products_state.freezed.dart';

@freezed
sealed class ProductsState with _$ProductsState {
  const factory ProductsState.initial()                           = ProductsInitial;
  const factory ProductsState.loading()                           = ProductsLoading;
  const factory ProductsState.loaded(List<Product> products)      = ProductsLoaded;
  const factory ProductsState.failure(Failure failure)            = ProductsFailure;
  // Estado granular: recarga manteniendo datos anteriores
  const factory ProductsState.refreshing(List<Product> products)  = ProductsRefreshing;
}
```

---

## Cubit con TaskEither — patrón recomendado para lógica simple

```dart
// features/products/presentation/cubit/products_cubit.dart

class ProductsCubit extends Cubit<ProductsState> {
  ProductsCubit({required GetProductsUseCase getProducts})
      : _getProducts = getProducts,
        super(const ProductsState.initial());

  final GetProductsUseCase _getProducts;

  Future<void> loadProducts() async {
    emit(const ProductsState.loading());

    final result = await _getProducts().run();

    // fold en Cubit: Left → failure, Right → loaded
    result.fold(
      (failure) => emit(ProductsState.failure(failure)),
      (products) => emit(ProductsState.loaded(products)),
    );
  }

  Future<void> refresh() async {
    // Mantiene los productos actuales mientras recarga
    final current = switch (state) {
      ProductsLoaded(:final products) => products,
      ProductsRefreshing(:final products) => products,
      _ => <Product>[],
    };

    emit(ProductsState.refreshing(current));

    final result = await _getProducts().run();
    result.fold(
      (failure) => emit(ProductsState.failure(failure)),
      (products) => emit(ProductsState.loaded(products)),
    );
  }
}
```

---

## BLoC con eventos y TaskEither — para lógica compleja

```dart
// ─── Eventos ──────────────────────────────────────────────────────────────────

sealed class ProductsEvent {
  const ProductsEvent();
}
final class ProductsLoadRequested extends ProductsEvent {
  const ProductsLoadRequested();
}
final class ProductsRefreshRequested extends ProductsEvent {
  const ProductsRefreshRequested();
}
final class ProductDeleteRequested extends ProductsEvent {
  const ProductDeleteRequested(this.productId);
  final String productId;
}

// ─── BLoC ─────────────────────────────────────────────────────────────────────

class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  ProductsBloc({
    required GetProductsUseCase getProducts,
    required DeleteProductUseCase deleteProduct,
  })  : _getProducts = getProducts,
        _deleteProduct = deleteProduct,
        super(const ProductsState.initial()) {
    on<ProductsLoadRequested>(_onLoad);
    on<ProductsRefreshRequested>(_onRefresh);
    on<ProductDeleteRequested>(_onDelete);
  }

  final GetProductsUseCase _getProducts;
  final DeleteProductUseCase _deleteProduct;

  Future<void> _onLoad(
    ProductsLoadRequested event,
    Emitter<ProductsState> emit,
  ) async {
    emit(const ProductsState.loading());
    final result = await _getProducts().run();
    result.fold(
      (f) => emit(ProductsState.failure(f)),
      (p) => emit(ProductsState.loaded(p)),
    );
  }

  Future<void> _onRefresh(
    ProductsRefreshRequested event,
    Emitter<ProductsState> emit,
  ) async {
    final current = state is ProductsLoaded
        ? (state as ProductsLoaded).products
        : <Product>[];

    emit(ProductsState.refreshing(current));

    final result = await _getProducts().run();
    result.fold(
      (f) => emit(ProductsState.failure(f)),
      (p) => emit(ProductsState.loaded(p)),
    );
  }

  Future<void> _onDelete(
    ProductDeleteRequested event,
    Emitter<ProductsState> emit,
  ) async {
    final result = await _deleteProduct(event.productId).run();

    result.fold(
      (f) => emit(ProductsState.failure(f)),
      (_) {
        // Remueve optimistamente de la lista actual
        if (state is ProductsLoaded) {
          final updated = (state as ProductsLoaded)
              .products
              .where((p) => p.id != event.productId)
              .toList();
          emit(ProductsState.loaded(updated));
        }
      },
    );
  }
}
```

---

## Widget: BlocBuilder con estado sellado

```dart
BlocBuilder<ProductsBloc, ProductsState>(
  builder: (context, state) => switch (state) {
    ProductsInitial()       => const SizedBox.shrink(),
    ProductsLoading()       => const Center(child: CircularProgressIndicator()),
    ProductsLoaded(:final products) => ProductsListView(products: products),
    ProductsRefreshing(:final products) => Stack(
        children: [
          ProductsListView(products: products),
          const Positioned(
            top: 0, left: 0, right: 0,
            child: LinearProgressIndicator(),
          ),
        ],
      ),
    ProductsFailure(:final failure) => FailureView(
        failure: failure,
        onRetry: () => context.read<ProductsBloc>().add(
          const ProductsLoadRequested(),
        ),
      ),
  },
)
```

---

## BlocListener para side effects de error

```dart
BlocListener<ProductsBloc, ProductsState>(
  listenWhen: (prev, curr) => curr is ProductsFailure,
  listener: (context, state) {
    if (state is ProductsFailure) {
      final l = AppLocalizations.of(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            state.failure.localizedMessage(context), // i18n
          ),
          backgroundColor: Theme.of(context).colorScheme.error,
          action: state.failure.isRetryable
              ? SnackBarAction(
                  label: l.retryButton, // traducido desde el ARB
                  onPressed: () => context.read<ProductsBloc>()
                      .add(const ProductsLoadRequested()),
                )
              : null,
        ),
      );
    }
  },
  child: BlocBuilder<ProductsBloc, ProductsState>(/* ... */),
)
```
