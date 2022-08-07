docker_build:
	docker build --tag backend .

docker_run:
	docker run -v ${PWD}/data:/backend/data -v ${PWD}/data:/backend/data -p 8000:8000 --rm backend

lint:
	docker run --rm --volume ${PWD}/app:/src --workdir /src pyfound/black:latest_release black --check .
