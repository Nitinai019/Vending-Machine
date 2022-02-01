# Vending-Machine

Quickstart
----------


1. create ``.env`` file in the processing directory.
 and set environment variables for application:
    ```
        touch .env
        echo DATABASE_URL=postgresql://postgres:password@db:5432/vending >> .env
    ```
2. Then use command for change file permission.
    ```
        chmod +x processing/db/01-init.sh 
    ```

3. run application
    ```
        docker-compose up
    ```

4. Application will be available on ``localhost`` in your browser.
    ```
        http://localhost:8000/docs
    ```

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.



Run tests
---------
1. start application on docker
    ```
    docker-compose up
    ```
2. open new command line tab and exec in processing_vending container
    ```
        docker exec -ti processing_vending_1 bash
    ```
3. in code directory run command for run tests
    ```
        pytest
    ```