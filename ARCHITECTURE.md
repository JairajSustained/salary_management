GET    /api/employees/          → list all (with pagination)
POST   /api/employees/          → create employee
GET    /api/employees/{id}/     → retrieve one employee
PUT    /api/employees/{id}/     → update employee (full)
PATCH  /api/employees/{id}/     → update employee (partial)
DELETE /api/employees/{id}/     → mark inactive (soft delete)

GET    /api/employees/insights/ → salary insights (min, max, avg by country/job title)
POST   /api/employees/import/   → seed/import 10k employees

## Future Improvements
- Add JWT authentication for API security
- Role based access control (Admin, Viewer)