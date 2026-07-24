# Basic Tutorials

## Onboard a new task type

The RMF2 Scheduler allows the user to define how a **task is converted into an element
in the BehaviorTree**.

Below is an example of how this can be done using the Scheduler Python API.

First define a custom `TaskExecutor`.

```python
from rmf2_scheduler import TaskExecutor, ExecutorData
from rmf2_scheduler.data import Task

class MyAwesomeTaskExecutor(TaskExecutor):
    def __init__(self):
        super().__init__()

    def build(self, task: Task):
        executor_data = ExecutorData();
        coorindates = task.task_details["coordinates"]
        asset_name = task.resource_id
        out = (
            "SubTree " +
            f"ID=\"ReplaceMAPF\" task_id=\"{task.id}\" " +
            "bt_id=\"{bt_id}\" task_status=\"{task_status}\" connection=\"{connection}\" " +
            f"coordinates=\"{coorindates}\" " +
            f"asset_name=\"{asset_name}\""
        )
        executor_data.set_data_as_string(out)
        return True, None, executor_data

    def start(self, id: str, executor_data: ExecutorData):  # Currently not used
        return True, "Undefined"
```

Then in `app.py` (under `src/rmf2_scheduler/demos/rmf2_scheduler_server`), add in the
following line.

```python
task_executors = {
    "ihi/go_to_amr": GoToAMRTaskExecutor(),
    "ihi/wait_amr": WaitAMRTaskExecutor(),
    "ihi/warehouse_task": WareHouseTaskExecutor(),
    "rmf2/mapf": MAPFTaskExecutor(),
    "ihi/dummy": DummyTaskExecutor(),
    "my_new_task_type": MyAwesomeTaskExecutor(),
}
```

## REST API Endpoints

Please make sure **Installation - IOCS Robot Task Generator & Scheduler** is completed,
and the RMF2 Scheduler Server is running at <http://localhost:8079>.

The endpoints swagger can be accessed at <http://localhost:8079/docs>.

### Create a task using REST Endpoints

> [!NOTE]
> Please make sure a RMF2 Scheduler Server is running. For more, check out the
> **Quick Start** in the [`rmf2_scheduler` docs](https://rmf-scheduler.readthedocs.io/).

Let's create a **Task** in the scheduler using the `POST /schedule/edit` API
and the `TASK_ADD` **ScheduleAction**.

This tutorial requires some utility command line tools. Run the following command
to install them.

```bash
sudo apt install coreutils curl uuid-runtime jq
```

**Step 1 - Dry run**

Let's do a **dry-run** of the REST API query. This checks if the query is valid.
No changes are made to the schedule stored.

Run the following cURL command.

```bash
curl --location 'localhost:8000/schedule/edit' \
     --header 'Content-Type: application/json' \
     --data-raw '{
       "type": "TASK_ADD",
       "task": {
         "id": "'$(uuidgen)'",
         "start_time": "'$(date -u -Iseconds)'",
         "type": "rmf2/dummy"
       }
     }'
```

You should receive a successful response as follows.

```
{"message":"Dry run successfully."}
```

**Step 2 - add task**

Let's run the command with **dry-run disabled**. This command changes the schedule
stored. Simply append query parameter `dry_run=false` to the URL.

`localhost:8000/schedule/edit?dry_run=false`

The full cURL command is as follows.

```bash
curl --location 'localhost:8000/schedule/edit?dry_run=false' \
     --header 'Content-Type: application/json' \
     --data-raw '{
       "type": "TASK_ADD",
       "task": {
         "id": "'$(uuidgen)'",
         "start_time": "'$(date -u -Iseconds)'",
         "type": "rmf2/dummy"
       }
     }'
```

Upon success, you should receive the following response.

```
{"message":"Schedule updated successfully!"}
```

**Step 3 - Verification**

Let's verify the task we have created.

To retrieve the task we have created, you can use the `GET /schedule/` API.

Simply run the following cURL command.

```bash
curl -sS localhost:8000/schedule/ | jq .
```

You should receive a response similar to the following.

```json
{
  "tasks": [
    {
      "type": "rmf2/dummy",
      "start_time": "2025-04-21T10:28:10Z",
      "id": "d37b295a-6fbc-431c-a87d-ece7607c9f89",
      "status": ""
    }
  ],
  "processes": []
}
```

> [!NOTE]
> RMF2 scheduler interprets and stores time in UTC timezone by default. The time
> output follows the [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601).

