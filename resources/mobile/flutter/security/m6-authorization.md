# M6. Autorización Insegura

Esta categoría cubre problemas de control de acceso y autorización implementados incorrectamente en el cliente.

---

## Check M6-A: Controles de autorización solo en la UI

**ID:** `M6-A-CLIENT-SIDE-AUTHZ`  
**Objetivo:** Detectar lógica de autorización implementada solo en el cliente sin validación en backend.  
**Ámbito:** `lib/**.dart`

**Método de búsqueda:** Semantic search  
**Patterns inseguros:**

```dart
// PATRÓN 1: Verificación de rol solo en UI
class UserProfile {
  String role;  // 'admin', 'user', 'guest'
}

Widget build(BuildContext context) {
  // ❌ Control de acceso solo visual
  if (currentUser.role == 'admin') {
    return AdminPanel();
  } else {
    return UserDashboard();
  }
}

// PATRÓN 2: Ocultar botones según rol (sin validación backend)
Widget deleteButton() {
  // ❌ Solo ocultar UI no es seguridad
  if (isAdmin) {
    return ElevatedButton(
      onPressed: () => deleteUser(userId),  // API no valida si es admin
      child: Text('Eliminar'),
    );
  }
  return SizedBox.shrink();
}

// PATRÓN 3: Modificar datos localmente sin validación
Future<void> updateUserRole(String userId, String newRole) async {
  // ❌ Cambiar rol localmente sin verificación backend
  userList.firstWhere((u) => u.id == userId).role = newRole;
  
  // Envía al API sin que el backend valide permisos
  await api.updateUser(userId, {'role': newRole});
}

// PATRÓN 4: Verificar permisos con datos del cliente
bool canDeletePost(Post post) {
  // ❌ Decisión basada en datos locales manipulables
  return post.authorId == currentUser.id || currentUser.isAdmin;
}

// PATRÓN 5: Endpoints sensibles sin headers de autorización
Future<void> deleteUser(String userId) async {
  // ❌ No incluye token en operación sensible
  await http.delete(Uri.parse('https://api.example.com/users/$userId'));
}
```

**Búsqueda lexical:**
```regex
if\s*\([^)]*\.(role|isAdmin|permission)\s*==
\.role\s*=\s*['\"]admin['\"](?!.*await.*api)
canDelete|canEdit|canView.*return.*currentUser
http\.(delete|put|patch).*(?!.*headers.*Authorization)
```

**Criterio:**
- ❌ **Falla:** Decisiones de autorización basadas solo en estado del cliente
- ❌ **Falla:** API calls sensibles sin token de autorización
- ⚠️ **Advertencia:** UI oculta funcionalidad pero API no valida permisos
- ✅ **Cumple:** Todas las operaciones validadas por backend

**Severidad:** `HIGH`  
**Automatización:** 🟡 Media (50%)

**Remediación:**

```dart
// ✅ SOLUCIÓN 1: Autorización validada por backend
class SecureApiService {
  final String _baseUrl = 'https://api.example.com';
  final AuthService _authService;
  
  SecureApiService(this._authService);
  
  // ✅ SIEMPRE incluir token en operaciones sensibles
  Future<bool> deleteUser(String userId) async {
    final token = await _authService.getValidAccessToken();
    
    if (token == null) {
      throw UnauthorizedException('No autenticado');
    }
    
    try {
      final response = await http.delete(
        Uri.parse('$_baseUrl/users/$userId'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );
      
      // ✅ Backend valida si el usuario tiene permiso
      if (response.statusCode == 200) {
        return true;
      } else if (response.statusCode == 403) {
        throw ForbiddenException('No tienes permisos para eliminar usuarios');
      } else {
        throw ApiException('Error al eliminar usuario');
      }
    } catch (e) {
      rethrow;
    }
  }
  
  // ✅ Obtener permisos desde backend
  Future<UserPermissions> getUserPermissions() async {
    final token = await _authService.getValidAccessToken();
    
    final response = await http.get(
      Uri.parse('$_baseUrl/user/permissions'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      // ✅ Permisos validados por backend
      return UserPermissions.fromJson(jsonDecode(response.body));
    }
    
    throw Exception('No se pudieron obtener permisos');
  }
}
```

```dart
// ✅ SOLUCIÓN 2: UI reactiva a permisos del backend
class PermissionController extends GetxController {
  final SecureApiService _apiService;
  
  final permissions = Rx<UserPermissions?>(null);
  
  PermissionController(this._apiService);
  
  @override
  void onInit() {
    super.onInit();
    loadPermissions();
  }
  
  // ✅ Cargar permisos desde backend
  Future<void> loadPermissions() async {
    try {
      permissions.value = await _apiService.getUserPermissions();
    } catch (e) {
      print('Error loading permissions: $e');
    }
  }
  
  // ✅ Verificar permisos (pero backend SIEMPRE valida)
  bool canDeleteUsers() {
    return permissions.value?.canDeleteUsers ?? false;
  }
}

// ✅ UI usa permisos pero backend valida
class UserListScreen extends StatelessWidget {
  final PermissionController permController = Get.find();
  final SecureApiService apiService;
  
  @override
  Widget build(BuildContext context) {
    return Obx(() {
      // ✅ Mostrar botón si tiene permiso (UX)
      if (permController.canDeleteUsers()) {
        return IconButton(
          icon: Icon(Icons.delete),
          onPressed: () async {
            try {
              // ✅ Backend valida el permiso nuevamente
              await apiService.deleteUser(userId);
              showSuccess('Usuario eliminado');
            } on ForbiddenException catch (e) {
              // Backend rechazó la operación
              showError(e.message);
            }
          },
        );
      }
      
      return SizedBox.shrink();
    });
  }
}
```

```dart
// ✅ SOLUCIÓN 3: Modelo de permisos desde backend
class UserPermissions {
  final bool canDeleteUsers;
  final bool canEditUsers;
  final bool canViewReports;
  final bool canManageRoles;
  final List<String> allowedResources;
  
  UserPermissions({
    required this.canDeleteUsers,
    required this.canEditUsers,
    required this.canViewReports,
    required this.canManageRoles,
    required this.allowedResources,
  });
  
  factory UserPermissions.fromJson(Map<String, dynamic> json) {
    return UserPermissions(
      canDeleteUsers: json['can_delete_users'] ?? false,
      canEditUsers: json['can_edit_users'] ?? false,
      canViewReports: json['can_view_reports'] ?? false,
      canManageRoles: json['can_manage_roles'] ?? false,
      allowedResources: List<String>.from(json['allowed_resources'] ?? []),
    );
  }
  
  // ✅ Verificación granular
  bool canAccessResource(String resourceId) {
    return allowedResources.contains(resourceId);
  }
}
```

```dart
// ✅ SOLUCIÓN 4: Interceptor que agrega token automáticamente
class AuthInterceptor extends Interceptor {
  final AuthService _authService;
  
  AuthInterceptor(this._authService);
  
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // ✅ Agregar token a TODAS las requests
    final token = await _authService.getValidAccessToken();
    
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    
    handler.next(options);
  }
  
  @override
  void onError(DioError err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 403) {
      // ✅ Manejar forbidden (sin permisos)
      _showPermissionDeniedDialog();
    }
    
    handler.next(err);
  }
  
  void _showPermissionDeniedDialog() {
    Get.dialog(
      AlertDialog(
        title: Text('Acceso denegado'),
        content: Text('No tienes permisos para realizar esta acción'),
        actions: [
          TextButton(
            onPressed: () => Get.back(),
            child: Text('OK'),
          ),
        ],
      ),
    );
  }
}
```

```dart
// ✅ SOLUCIÓN 5: Logging de intentos de acceso no autorizado
class SecurityLogger {
  static void logUnauthorizedAttempt(String action, String resourceId) {
    final event = {
      'timestamp': DateTime.now().toIso8601String(),
      'action': action,
      'resource_id': resourceId,
      'user_id': currentUserId,
      'device_id': deviceId,
    };
    
    // ✅ Enviar al backend para auditoría
    _sendSecurityEvent(event);
    
    // También registrar localmente (opcional)
    print('SECURITY: Unauthorized attempt - $event');
  }
  
  static Future<void> _sendSecurityEvent(Map<String, dynamic> event) async {
    try {
      await http.post(
        Uri.parse('https://api.example.com/security/events'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode(event),
      );
    } catch (e) {
      print('Error sending security event: $e');
    }
  }
}
```

---

## Mejores Prácticas de Autorización

### ✅ DO (Hacer)
1. **SIEMPRE validar permisos en el backend**
2. Usar tokens JWT con claims de permisos
3. Implementar RBAC (Role-Based Access Control) en backend
4. Recargar permisos periódicamente desde backend
5. Manejar correctamente respuestas 403 Forbidden
6. Logging de intentos de acceso no autorizado

### ❌ DON'T (No hacer)
1. NUNCA confiar en verificaciones solo en cliente
2. No ocultar solo UI sin proteger API
3. No almacenar roles/permisos en SharedPreferences
4. No tomar decisiones de seguridad con datos locales
5. No modificar permisos localmente sin validación backend

---

## Resumen M6

| Check | Severidad | Automatización | Esfuerzo Fix |
|-------|-----------|----------------|--------------|
| M6-A | HIGH | 🟡 50% | Alto |

**Total checks:** 1  
**Severidad crítica:** 0  
**Severidad alta:** 1  
**Severidad media:** 0  
**Severidad baja:** 0

---

**Última actualización:** 2025-11-12  
**Versión:** 1.0