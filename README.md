# Small business: microservices

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit hooks](https://github.com/BarabanovaIrina/small_business_ms/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/BarabanovaIrina/small_business_ms/actions)
[![Tests](https://github.com/BarabanovaIrina/small_business_ms/actions/workflows/run_tests.yml/badge.svg)](https://github.com/BarabanovaIrina/small_business_ms/actions)

## Project description

Create a single API that seamlessly exposes the data
of three different systems: Warehouse, Accounting, Sales.
The system should be available 24/7, scalable, resilient to failures,
and the data should be available through different offices around the world.

### Mian requirements

- ~~Design the architecture of the new system and explain your reasons to use it~~
- ~~Code at least three microservices with the best code quality possible
  and expose them via a REST API~~
- ~~The software artifacts should be covered by unit tests~~
- ~~The software artifacts should be easy to package and deploy~~

### Extra requirements

- ~~Provide any document or diagram useful to explain your proposal~~
- Applications covered by acceptance tests suites
- ~~Define the software technologies that should be used to build a system
  that’s scalable, reliable, and distributed.~~
- Describe your ideal development workflow considering stability, security,
  and agility from the beginning.
- Define a versioning policy and a strategy to deploy in production
- Automatically generated documentation
- Mention the software technologies to build your ideal CI/CD environment
- ~~Fully functional CI workflow~~
- Fully functional CD workflow

## Design

Stack: Python, Django, Postgres, Kubernetes

**Why Django?** Personal curiosity, because I've never worked with it.

**Why Kubernetes?** Kubernetes allows easily scale services and make clear
intra-service communication.

**Why Postgres?** This is the most common enterprise DB solution.

### What is planned to be Done:

The whole system is supposed to be deployed in a Kubernetes cluster and have cluster
API Gateway to all the services.

![Design](docs/images/architecture.png)

### What is Done at the moment

<table border="0">
 <tr>
    <td><b style="font-size:20px">Service</b></td>
    <td><b style="font-size:20px">Deploy</b></td>
 </tr>
 <tr>
    <td>Each service has several layers, which are flexible to extend and replace.

![Layers](docs/images/layers.png)</td>

<td>Each service(django project) has the following files to be able to work with
other services within a Kubernetes cluster:

![Layers](docs/images/deployment.png)</td>

 </tr>
</table>

**Intra-service communication**

At the moment, the is only one intra-service communication between
Sales and Warehouse which is accessible via the following endpoint:

```shell
curl "http://<GATEWAY_IP>:<GATEWAY_PORT>/sales/sold_items"
```

There is a [Postman collection](https://github.com/BarabanovaIrina/small_business_ms/tree/docs/docs/postman/small_business.postman_collection.json) with all the available(at the moment) requests.

### What is yet to be Done:

- Replace dummy Dict database with a real Postgres database
- Extend CRUD for other services
- Come up with a Scenario of using message bus in intra-service communication
- Create CD pipelines
- Add autodocumentation
