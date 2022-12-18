docker_build:
	docker build --tag backend .

docker_run:
	docker run -v ${PWD}/data:/backend/data -p 8000:8000 --rm backend

docker_dev_build:
	docker build --tag backend-dev --file Dockerfile-dev .

lint:
	docker run -v ${PWD}/app:/backend/app --rm backend-dev /bin/bash -c "isort app;black app;pylint app"
