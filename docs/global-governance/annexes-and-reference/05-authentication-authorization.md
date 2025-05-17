# Chapter 5: Authentication & Authorization

In the last chapter, you learned how to call external helpers with [Agent Integration](04_agent_integration_.md). Now it’s time to lock things down so only the right people—or AI agents—can see or change sensitive data.  

---

## 1. Why Do We Need Authentication & Authorization?

Imagine a citizen applies for housing benefits.  
- Anytime they log in, we must **confirm it’s really them** (Authentication).  
- Once logged in, only staff in the “Benefits Officer” role (not every clerk) should **approve** applications (Authorization).

Without this security layer:
- Personal data could be leaked.  
- Unauthorized edits could happen.  
- Audit trails and privacy protections break.

Think of it like government security clearances:  
- **Authentication** is showing your ID badge at the door.  
- **Authorization** is having the right clearance level to enter certain rooms.

---

## 2. Key Concepts

1. **Authentication**  
   Verifies who you are—username/password or tokens.

2. **Authorization**  
   Checks what you’re allowed to do—roles, permissions, or policies.

3. **Tokens & Sessions**  
   After login, you get a session or a token (e.g. Laravel Sanctum) to prove you’re authenticated on each request.

4. **Middleware & Policies**  
   Code layers that automatically enforce auth checks before running your controller logic.

---

## 3. Applying Authentication in HMS-API

### 3.1 Protecting a Route

In `routes/api.php`, wrap your sensitive endpoints in an `auth:sanctum` middleware:

```php
use Illuminate\Http\Request;

Route::middleware('auth:sanctum')->group(function(){
  Route::get('/benefits/applications', function(Request $req){
    return \App\Models\BenefitApplication::all();
  });
});
```

Explanation:
- `auth:sanctum` ensures only valid token-holders get through.
- If the token’s missing or expired, Laravel returns `401 Unauthorized`.

### 3.2 Logging In & Getting a Token

A simple login controller:

```php
class AuthController extends Controller
{
  public function login(Request $req)
  {
    // 1. Check credentials
    if (!Auth::attempt($req->only('email','password'))) {
      return response()->json(['error'=>'Invalid'], 401);
    }
    // 2. Create a token
    $token = $req->user()->createToken('api-token')->plainTextToken;
    return ['token'=>$token];
  }
}
```

Explanation:
1. `Auth::attempt()` checks email/password.  
2. On success, `createToken()` makes a personal access token.  

Now the client sends:
```
Authorization: Bearer your-generated-token
```
on each request.

---

## 4. Adding Authorization Rules

### 4.1 Roles on the User Model

In `app/Models/User.php`, allow a `role` field:

```php
class User extends Authenticatable
{
  protected $fillable = ['name','email','password','role'];
}
```

When you register or seed users, set `role` to `'admin'`, `'officer'`, or `'citizen'`.

### 4.2 Defining a Policy

Create `app/Policies/BenefitApplicationPolicy.php`:

```php
class BenefitApplicationPolicy
{
  // Can this user approve applications?
  public function approve(User $user)
  {
    return $user->role === 'officer';
  }
}
```

Register it in `AuthServiceProvider.php`:

```php
protected $policies = [
  \App\Models\BenefitApplication::class
    => \App\Policies\BenefitApplicationPolicy::class,
];
```

### 4.3 Using the Policy in a Controller

```php
class BenefitController extends Controller
{
  public function approve($id)
  {
    $app = BenefitApplication::findOrFail($id);
    $this->authorize('approve', $app);
    $app->status = 'approved';
    $app->save();
    return response()->json($app);
  }
}
```

Explanation:
- `$this->authorize('approve', $app)` throws `403 Forbidden` if the user lacks permission.

---

## 5. Under the Hood: Sequence of a Secure Request

```mermaid
sequenceDiagram
  participant UI as Front-End
  participant API as HMS-API
  participant Auth as AuthService
  participant DB as Database

  UI->>API: POST /login {email,password}
  API->>Auth: attempt()
  Auth->>DB: SELECT user
  DB-->>Auth: user record
  Auth-->>API: success
  API-->>UI: {token}

  UI->>API: GET /benefits/applications (Bearer token)
  API->>Auth: validate token
  Auth->>DB: find token
  DB-->>Auth: token valid
  Auth-->>API: authenticated
  API->>Controller: authorize('viewAny', Application)
  Controller-->>API: allowed?
  API-->>UI: 200 OK + data
```

1. **Login**: user gets a token.  
2. **Token Check**: middleware validates it on each call.  
3. **Policy Check**: before sensitive methods, Laravel calls your policy.  

---

## 6. Deeper Dive: Auth Middleware & Policy Binding

### 6.1 Laravel’s Auth Middleware

File: `vendor/laravel/sanctum/src/Guard.php` (simplified):

```php
public function user()
{
  // Read “Authorization” header
  // Find token in the database
  // Return the corresponding User model
}
```

### 6.2 Policy Resolution

In `Illuminate\Auth\Access\Gate`:

```php
public function authorize($ability, $model)
{
  $policy = $this->getPolicyFor($model);
  return $policy->{$ability}(Auth::user(), $model);
}
```

Laravel maps your model to `BenefitApplicationPolicy` and calls your method.

These internals ensure that your simple `approve()` rule runs automatically.

---

## Conclusion

You now know how to:

- **Authenticate** users and agents with tokens  
- **Authorize** actions using roles and policies  
- Protect routes and controllers in HMS-API  

Next, we’ll explore how to design and document your actual **[Backend API Endpoints](06_backend_api_endpoints_.md)** so clients can call these secure operations correctly.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)