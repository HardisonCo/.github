# Chapter 8: CodifySubprojects

In the last chapter, you learned how HMS-API keeps each agency’s data separated with **[Tenant Management](07_tenant_management_.md)**. Now we’ll see how to break large initiatives into focused, manageable sub-units called **Subprojects**—think of them as task forces or working groups within a broader program.

---

## 1. Why Do We Need Subprojects?

Imagine your “No Poverty” program is so big it’s hard to track everything at once. You might create three subprojects:

- **Affordable Housing Task Force**  
- **Job Training Working Group**  
- **Food Security Coalition**

Each group has its own objectives, budget, and timeline. By codifying subprojects, you:

- Assign clear goals and resources  
- Let different teams work in parallel  
- Track progress at a finer granularity  

This keeps the big picture organized and each team accountable.

---

## 2. Key Concepts

1. **Subproject**  
   A child of a Program, with its own name, description, objectives, and resource allocation.

2. **Program Relationship**  
   Every Subproject belongs to one [Program Model](01_program_model_.md).

3. **Tenant Context**  
   Like Programs, Subprojects are tied to a tenant so agencies can’t see each other’s subprojects.

4. **API Endpoints**  
   You’ll call `/programs/{program}/subprojects` to manage these units.

---

## 3. Defining the Subproject Model

### 3.1 Database Migration

Create a migration to store subprojects:

```php
// database/migrations/2024_xx_xx_create_subprojects_table.php
Schema::create('subprojects', function (Blueprint $table) {
  $table->id();
  $table->foreignId('program_id')->constrained()->cascadeOnDelete();
  $table->foreignId('tenant_id')->index();
  $table->string('name');
  $table->text('objectives')->nullable();
  $table->decimal('budget', 12, 2)->nullable();
  $table->timestamps();
});
```

This sets up the `subprojects` table with links to a Program and a Tenant.

### 3.2 Eloquent Model

```php
// app/Models/Core/Subproject/Subproject.php
namespace App\Models\Core\Subproject;

use Illuminate\Database\Eloquent\Model;

class Subproject extends Model
{
  protected $fillable = [
    'program_id','tenant_id','name','objectives','budget'
  ];

  public function program()
  {
    return $this->belongsTo(\App\Models\Core\Program\Program::class);
  }

  protected static function booted()
  {
    // Automatically scope queries by current tenant
    static::addGlobalScope('tenant', function($q){
      $q->where('tenant_id', app(\App\Models\Tenant::class)->id);
    });
  }
}
```

- `fillable` lets us mass-assign core fields.
- `program()` links back to the parent Program.
- The global scope ensures we only see subprojects for our current tenant.

---

## 4. Exposing Subprojects via API

### 4.1 Routes

Add these in `routes/api.php` under your `auth:sanctum` and `TenantMiddleware` group:

```php
Route::get('/programs/{program}/subprojects', [SubprojectController::class,'index']);
Route::post('/programs/{program}/subprojects', [SubprojectController::class,'store']);
Route::put('/subprojects/{id}',              [SubprojectController::class,'update']);
Route::delete('/subprojects/{id}',           [SubprojectController::class,'destroy']);
```

### 4.2 Controller Methods

```php
// app/Http/Controllers/SubprojectController.php
public function index(Program $program)
{
  return response()->json($program->subprojects);
}

public function store(SubprojectRequest $req, Program $program)
{
  $data = $req->validated() + [
    'tenant_id'  => app(\App\Models\Tenant::class)->id,
    'program_id' => $program->id
  ];
  $sub = \App\Models\Core\Subproject\Subproject::create($data);
  return response()->json($sub, 201);
}
```

- **index** returns all subprojects under a given Program.  
- **store** validates input, adds `tenant_id` and `program_id`, then creates a Subproject.

#### Input Validation

```php
// app/Http/Requests/SubprojectRequest.php
public function rules()
{
  return [
    'name'       => 'required|string|max:255',
    'objectives' => 'nullable|string',
    'budget'     => 'nullable|numeric|min:0'
  ];
}
```

This ensures every new Subproject has a name and sensible optional fields.

---

## 5. Real-World Flow

When a program manager clicks **“Add Subproject”**, here’s what happens:

```mermaid
sequenceDiagram
  participant FE as Front-End
  participant API as HMS-API
  participant Val as Validator
  participant DB as Database

  FE->>API: POST /programs/1/subprojects
    {name:"Housing TF",objectives:"Build 500 units"}
  API->>Val: validate request
  Val-->>API: success
  API->>DB: INSERT INTO subprojects ...
  DB-->>API: new record {id:10,...}
  API-->>FE: 201 Created {id:10,name:"Housing TF",...}
```

1. **FE** submits form data.  
2. **API** runs `SubprojectRequest` rules.  
3. On success, Eloquent saves the record with the current tenant.  
4. **FE** sees the newly created Subproject.

---

## 6. Under the Hood: How It All Fits

1. **Routing & Middleware**  
   - `auth:sanctum` checks you’re logged in.  
   - `TenantMiddleware` reads `X-Tenant-Code` and binds the Tenant instance.

2. **Global Scopes**  
   - Both `Program` and `Subproject` models use a tenant scope, so you never see data from other agencies.

3. **Eloquent Relationships**  
   - `Program::subprojects()` lets you fetch every subproject for that program.

4. **Validation & Storage**  
   - `SubprojectRequest` enforces data shape.  
   - `Subproject::create()` handles the SQL `INSERT` for you.

---

## Conclusion

You’ve now learned how to **codify Subprojects** in HMS-API:

- Defined a **Subproject** model and migration  
- Scoped data by **Tenant** for isolation  
- Set up **API routes** and **controller** actions  
- Created **FormRequests** to validate inputs  
- Viewed the **sequence** of a subproject creation  

With subprojects in place, you can organize any large policy into clear, trackable task forces. Next up, we’ll see how to roll out those policies into live environments using **[Policy Deployment Mechanism](09_policy_deployment_mechanism_.md)**.

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)