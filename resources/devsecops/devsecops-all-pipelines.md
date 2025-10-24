---
title: Catálogo de Pipelines DevSecOps
type: mcp-resource-list
version: 1.0
description: >
	Lista de pipelines DevSecOps reutilizables, con descripción y URL de acceso, para integración automatizada vía servidor MCP.
artifacts:
	- name: devsecops-ci-pipe-yml-build-docker
		description: Plantillas de pipeline Azure DevOps para análisis estático y construcción automatizada de imágenes Docker.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-build-docker.git
	- name: devsecops-ci-pipe-yml-build-java-gradle
		description: Pipeline CI/CD para proyectos Java con Gradle, integrando análisis estático, build y testing.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-build-java-gradle.git
	- name: devsecops-ci-pipe-yml-build-layers-aws
		description: Automatiza la construcción, empaquetado y publicación de AWS Lambda Layers reutilizables.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-build-layers-aws.git
	- name: devsecops-ci-pipe-yml-build-node-npm
		description: Pipeline CI/CD para Node.js con NPM, integrando análisis estático y seguridad.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-build-node-npm.git
	- name: devsecops-ci-pipe-yml-build-node-yarn
		description: Pipeline Azure DevOps para automatizar construcción, testing y análisis estático con Yarn y Node.js/TypeScript.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-build-node-yarn.git
	- name: devsecops-ci-pipe-yml-build-python-pip
		description: Pipeline CI/CD para proyectos Python, con análisis estático, pruebas y empaquetado.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-build-python-pip.git
	- name: devsecops-ci-pipe-yml-inventory-ms
		description: Templates de Azure DevOps para análisis estático e integración continua de microservicios y control de inventario.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-inventory-ms.git
	- name: devsecops-ci-pipe-yml-naming-rules-validation
		description: Pipeline para validar nombres de ramas y mensajes de commit en Azure DevOps.
		url: git@github.com:somospragma/devsecops-ci-pipe-yml-naming-rules-validation.git
	- name: devsecops-sast-pipe-yml-checkov-iac
		description: Pipeline automatizado para análisis de seguridad de Infraestructura como Código (IaC) usando Checkov.
		url: git@github.com:somospragma/devsecops-sast-pipe-yml-checkov-iac.git
