.PHONY: dev build push deploy test

dev:
	docker-compose up --build

test:
	pytest tests/ -v

build:
	docker build -t kubeops-api:latest services/kubeops-api/
	docker build -t kubeops-ui:latest services/kubeops-ui/

push:
	./ci-cd/scripts/build-push.sh

deploy:
	./ci-cd/scripts/deploy.sh

logs:
	kubectl logs -n kubeintel -l app=kubeops-api -f

status:
	kubectl get pods,svc,hpa -n kubeintel
