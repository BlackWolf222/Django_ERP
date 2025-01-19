Django Backend Developer Exercise Documentation

  Steps to run the application locally
  
    Clone the Repository
      git clone {your-repo-url}
      cd {your-project-folder}

    Set up environment variables
      Create a .env file in the root and include the following variables:
        DEBUG=True
        SECRET_KEY=<your-secret-key>
        DB_NAME=django_db
        DB_USER=django_user
        DB_PASSWORD=django_password
        DB_HOST=db
        DB_PORT=5432

    Run the application with docker compose
        docker-compose up --build

      The command will build the application image, start the Django application and database container
      The backend will be exposed on localhost:8001

    Running database migrations
        docker-compose exec web python manage.py migrate

    Create Superuser(Optional)
        docker-compose exec web python manage.py createsuperuser

  API Documentation
  
    The backend is exposed on localhost:8001
        http://localhost:8000/api/

   Endpoints

   Endpoints for Company:
   
  1.List all Companies
    
       Endpoint: GET /api/company/
       Description: Retrives a list of all companies
       Response:
       
            [
              {
                "id": "5ef36830-a959-453e-aaa8-e6208c2b727d",
                "name": "MyCorp",
                "address": "123 Silicon Valley",
                "phone": "+1234567890",
                "description": "Leading tech company",
                "employee_count": 2
              },
              {
                "id": "4abd01fc-323d-453d-8939-10041d405e47",
                "name": "YourCorp",
                "address": "456 Silicon Valley",
                "phone": "+9876543210",
                "description": "Innovative tech company",
                "employee_count": 1,
                }
            ]
  2.List Companies with employees

         Endpoint: GET /api/company/?with_employees=1 (default is 0)
         Description: Retrives a list of all companies with detailed employee data
         Response:
         {
            "id": "5ef36830-a959-453e-aaa8-e6208c2b727d",
            "name": "MyCorp",
            "address": "123 Silicon Valley",
            "phone": "+1234567890",
            "description": "Leading tech company",
            "employee_count": 2,
            "employees": [
              {
                "id": "7da4daeb-8ffb-45d2-860a-b2c6742d18d1",
                "name": "Alice Johnson",
                "email": "alice@techcorp.com",
                "job_title": "developer",
                "age": 30
              },
              {
                "id": "74ab8e4c-e32d-486b-9fb1-8ae4de2483b1",
                "name": "Bob Smith",
                "email": "bob@techcorp.com",
                "job_title": "tester",
                "age": 28
              }
            ]
           }
  3.List a specific Company
  
          Endpoint: GET /api/company/<id>
          Description: Fetches details of a specific company by ID
          Response:
          {
            "id": "5ef36830-a959-453e-aaa8-e6208c2b727d",
            "name": "MyCorp",
            "address": "123 Silicon Valley",
            "phone": "+1234567890",
            "description": "Leading tech company",
            "employee_count": 2,
          }

  4.List a specific Company with detaild employee data
          
          Endpoint: GET /api/company/<id>?with_employees=1 (default is 0)
          Description: Fetches details of a specific company and its employees by ID
          Response:
          {
            "id": "5ef36830-a959-453e-aaa8-e6208c2b727d",
            "name": "MyCorp",
            "address": "123 Silicon Valley",
            "phone": "+1234567890",
            "description": "Leading tech company",
            "employee_count": 2,
            "employees": [
                {
                  "id": "7da4daeb-8ffb-45d2-860a-b2c6742d18d1",
                  "name": "Alice Johnson",
                  "email": "alice@techcorp.com",
                  "job_title": "developer",
                  "age": 30
                },
                {
                  "id": "74ab8e4c-e32d-486b-9fb1-8ae4de2483b1",
                  "name": "Bob Smith",
                  "email": "bob@techcorp.com",
                  "job_title": "tester",
                  "age": 28
                }
              ]
            }

  5.Create a company
  
          Endpoint: POST /api/company/
          Description: Creates a company
          Request Body:
          {
            "name": "FutureTech LLC",
            "address": "789 Innovation Blvd",
            "phone": "+1239876543",
            "description": "Revolutionizing technology",
          }
          
  6.Create a company with employees

          Endpoint: POST /api/company/
          Description: Creates a company
          Request Body:
          {
            "name": "MyCorp",
            "address": "123 Silicon Valley",
            "phone": "+1234567890",
            "description": "Leading tech company",
            "employees": [
              {
                "name": "Alice Johnson",
                "email": "alice@techcorp.com",
                "job_title": "developer",
                "age": 30
              },
              {
                "name": "Bob Smith",
                "email": "bob@techcorp.com",
                "job_title": "tester",
                "age": 28
              }
            ]
          }

  7.Update specific fields of a company
  
          Endpoint: PATCH /api/company/<id>
          Description: Updates specific fields of a company
          Request Body:
          {
            "phone": "+1234567890",
            "description": "New description",
          }
          
   8.Delete a company
   
           Endpoint: DELETE /api/company/<id>
           Description: Deletes a specific company
           Request Body:
           {}

   Additional note: PUT is not allowed for companies
  
  Endpoints for Employee:
  
1.List all employees
    
           Endpoint: GET /api/employee/
           Description: Retrieves a list of all employees
           Response:
            [
              {
                  "id": "af62b89e-fc1c-4f94-8123-c69f2428da8b",
                  "name": "Eve Summers",
                  "email": "eve@futuretech.com",
                  "job_title": "designer",
                  "age": 26,
                  "company": {
                  "id": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f",
                  "name": "FutureTech LLC"
                }
              },
              {
                  "id": "cd90f1e1-4747-45f3-bce6-5de7ec23b298",
                  "name": "John Doe",
                  "email": "john@futuretech.com",
                  "job_title": "manager",
                  "age": 40,
                  "company": {
                  "id": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f",
                  "name": "FutureTech LLC"
                }
              }
            ]

   2.List a specific employees
    
           Endpoint: GET /api/employee/<id>
           Description: Fetches details of a specific employee by ID
           Response:
              {
                  "id": "af62b89e-fc1c-4f94-8123-c69f2428da8b",
                  "name": "Eve Summers",
                  "email": "eve@futuretech.com",
                  "job_title": "designer",
                  "age": 26,
                  "company": {
                  "id": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f",
                  "name": "FutureTech LLC"
                }
   3.Create a new employee

           Endpoint: POST /api/employee/
           Description: Creates an employee
           Request Body:
            {
              "name": "Alice Brown",
              "email": "alice.brown@innovate.com",
              "job_title": "developer",
              "age": 29,
              "company": "5ef36830-a959-453e-aaa8-e6208c2b727d"
            }
      
  5.Update all fields of a specific employee
     
           Endpoint: PUT /api/employee/<id>
           Description: Updates all fields of an employee
           Request Body:
            {
              "name": "Alice Brown",
              "email": "alice.brown@innovate.com",
              "job_title": "developer",
              "age": 29,
              "company": "5ef36830-a959-453e-aaa8-e6208c2b727d"
            }
            
  6.Update specific fields of a specific employee
  
           Endpoint: PATCH /api/employee/<id>
           Description: Updates specific fields of a specific employee
           Request Body:
            {
              "name": "Brown Alice",
              "job_title": "tester",
              "age": 30
            }
            
  7.Delete an employee
  
           Endpoint: DELETE /api/employee/<id>
           Description: Deletes an employee
           Request Body:
           {}

  Endpoints for Empployee bulk:
  
1.Creates multiple employees in a single request
  
          Endpoint: POST /api/employee/bulk
          Description: Add multiple employees in a single request.
          Request Body:
          [
            {
              "name": "Charlie Adams",
              "email": "charlie@futuretech.com",
              "job_title": "tester",
              "age": 24,
              "company": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f"
            },
            {
              "name": "Dana Roberts",
              "email": "dana.roberts@futuretech.com",
              "job_title": "developer",
              "age": 31,
              "company": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f"
            }
          ]
          
  2.Update multiple employees in a single request
  
          Endpoint: PUT /api/employee/bulk
          Description: Update multiple employees in a single request
          Request Body:
          [
            {
              "id": "af62b89e-fc1c-4f94-8123-c69f2428da8b",
              "name": "Charlie Adams",
              "email": "charlie@futuretech.com",
              "job_title": "tester",
              "age": 24,
              "company": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f"
            },
            {
              "id": "cd90f1e1-4747-45f3-bce6-5de7ec23b298",
              "name": "Dana Roberts",
              "email": "dana.roberts@futuretech.com",
              "job_title": "developer",
              "age": 31,
              "company": "6c29492f-1a27-4b27-a2f5-cb8e8c582a0f"
            }
          ]
  3.Partially update specific fields of multiple employees
  
          Endpoint: PATCH /api/employee/bulk
          Description: Update multiple employees in a single request
          Request Body:
          [
            {
              "id": "af62b89e-fc1c-4f94-8123-c69f2428da8b",
              "company": "5ef36830-a959-453e-aaa8-e6208c2b727d"
            },
            {
              "id": "cd90f1e1-4747-45f3-bce6-5de7ec23b298",
              "job_title": "designer"
            }
          ]
          
  4. Delete multiple employees in a single request.
     
          Endpoint: DELETE /api/employee/bulk
          Description: Delete multiple employees in a single request.
          Request Body:
          [
            {"id":"af62b89e-fc1c-4f94-8123-c69f2428da8b"},
            {"id":"cd90f1e1-4747-45f3-bce6-5de7ec23b298"}
          ]

Additional Notes

  Database Configuration
      The project uses PostgreSQL as the database. Ensure the .env file matches your configuration.
      
  Testing
      Run all tests using:
      
        docker-compose exec web python manage.py test
        
  Admin Panel
    Access the admin panel to manage data manually. URL: http://localhost:8001/admin/.





















        
        
