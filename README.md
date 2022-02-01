# Vending-Machine

Quickstart
----------

1. go to processing/db directory and use command for change permission of file.
    ```
        chmod +x 01-init.sh 
    ```

2. Then create ``.env`` file in the processing directory.
 and set environment variables for application:
    ```
        touch .env
        echo DATABASE_URL=postgresql://postgres:password@db:5432/vending
    ```

3. run application
    ```
        docker-compose up
    ```


for stop process

```
    docker-compose down
```


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