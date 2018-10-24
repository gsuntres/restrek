## Restrek 

Restrek is a simple yet powerful api tool. It supports the programmer during the api development and at the same time provides mechanisms to facilitate end-to-end testing.



## Installation

```bash
git clone git@github.com:gsuntres/restrek.git
cd restrek
make install
```



## Initialize a project

Create a directory for your project



```bash
mkdir myproject
cd myproject
restrek-init
```

*Note: Check this [sandbox-project](https://github.com/gsuntres/restrek-sandbox-project) to quickly run and evaluate the sample project created by `restrek-ini`.*

 

Inspecting the newly created project directory structure you'll notice that  it has three main directories, the **commands**, **plans** and **envs** directories.



## Commands

Commands directory contains the api call definitions, in our example, `check`,  `post_call` and `delete_call` with the following definitions:



*commands/group1/check.yml*

```yaml
name: Check if API is alive
http: 
  url: /check
```



commands/group1/post.yml

```yaml
name: A post call that recieves a payload and returns it
http: 
  url: /post_call
  method: POST
```



commands/group1/delete.yml

```yaml
name: Delete an entity by id
http: 
  url: /delete_call/{{ delete__id }}
  method: DELETE
```



*Name* is a brief description of the call and *http* specifies which module to use. The module `http` has a number of properties namely:

* **host** - the target host (default: localhost)
* **secure** - is the target host secure or not (default: false)
* **timeout** - timeout in milliseconds (default: 1000)
* **url** - the url path (default: /)
* **method**: GET, POST, etc (default: GET)
* **headers**: define headers to use in requests
* **ssl_verify**: should verify certificates (default: true)

Since most properties are mainly the same between commands, common ones like host, secure, headers, etc can be defined in a separate file called  `properties`. More details about that in the next section.



## Environments

Predefined variables and the properties file exist in the target's environment directory. If no environment is specified `devel` is assumed. If needed we can add more environments like `staging` by simply creating the corresponding directory. Variables can be literals, objects or arrays and can be segregated into multiple files



#### properties

This files contains properties shared between commands. In our example the properties file is as follows:

```yaml
---
debug: True

http:
  host: localhost
  headers:
    "Content-Type": application/json;charset=utf-8
    "Accept": application/json;charset=utf-8
```



http specifies which properties to use when the http module is being used, which means that all the commands will also be using properties defined in here.



#### overriding properties

Although the main properties are defined in the environment's directory, they can be overridden when placed in a command's group directory. This way you are able to use commands that use different hosts for example. Such functionality is useful when dealing with micro-services or 3rd party apis such as an api gateway.



## Plans

Plans is where the actions begins! A plan can have one or multiple commands and they serve a dual role. They can be used to run a single command to test and evaluate the call being implemented, but they can also contain a series of steps to test business logic, etc.

In our example running `restrek-console` will bring up the main console where we can list and run our plans. Running `list groups` will return all available plan groups and `list plans` all available plans. You can run one or more plans by simple issuing a `run` command followed by the plans fully qualified names, separated by a space, in our example `run group1.test_api`.



#### plans and steps explained

Plans use one or more steps to accomplish their goals. Steps have three main parameters *command*, *register* and *tests*. Under the hood the command is being executed and its output becomes available to the rest of the parameters, the the tests, a list of assertions, run and finally the register assigns values to new or existing variables. Both register and tests have access to the command's output. The output of a command that uses the http module has the following structure:

* **status** - the http status code returned
* **body** - the body returned. *Note: if it's json is being parsed and returned as an object otherwise as a raw string*
* **headers** - a dictionary with the response's headers
* **cookies** - a dictionary with the response's cookies





So if we need, for example, to save the entity's name, we've just retrieved, we would do the following

```yaml
- command: mygroup.retrieve_entity
  register:
    myentity_name: body['name']
  tests:
  - assert_eq(200, status)
```



Now *myentity_name* is defined and globally available.



It is worth mentioning that register can be used alone within a step, usually to assign fixed values, like so

```yaml
- register:
    entity_status: active
- command: mygrou.retrieve_entity_by_status
```



*mygroup/retrieve_entity_by_status*

```yaml
name: Retrieve entity by status
http:
  url: /entity/{{ entity_status }}
```



Lastly we can use the *skip* parameter to skip a step, e.g.

```bash
- command: mygroup.retrieve_entity
  register:
    myentity_name: body['name']
  tests:
  - assert_eq(200, status)
  skip: yes
```



#### Restrek as a testing tool

When running the command `restrek` from within your project's root directory, the tool searches the plans directory for plans with *test_* as a prefix and executes them. The execution can be farther refined by using the `Trekfile` file.
