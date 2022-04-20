venv:
	python -m venv venv && \
	source venv/bin/activate && \
	python -m pip install --upgrade pip && \
	pip install -r requirements.txt

docker_build:
	docker build --tag backend .

docker_run:
	docker run -v ${PWD}/data:/backend/data -v ${PWD}/data:/backend/data -p 8000:8000 --rm backend
