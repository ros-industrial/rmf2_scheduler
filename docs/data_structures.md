## Task Data Structure

| Field                | Type    | Required | Description                                                                                                             |
| -------------------- | ------- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| `id`                 | string  | required | Task ID, in IOCS this is stored as `urn:<id>`                                                                           |
| `type`               | string  | required | Task type, this is used to distinguish execution methods. This can also be used for conflict checking and optimization. |
| `description`        | string  | optional | Additional description of the task.                                                                                     |
| `start_time`         | ISOTime | required | Start time of the task. This is updated to the actual start time once the task execution has started.                   |
| `end_time`           | ISOTime | optional | End time of the task. This is updated to the actual end time once the task execution has completed.                     |
| `process_id`         | string  | optional | The process this task belongs to.                                                                                       |
| `series_id`          | string  | optional | The reoccurring series the task belongs to. This is unused in IHI use cases.                                            |
| `status`             | string  | optional | The status of the task.                                                                                                 |
| `resource_id`        | string  | optional | The Resource ID assigned to this task.                                                                                  |
| `deadline`           | ISOTime | optional | The deadline of the task.                                                                                               |
| `planned_start_time` | ISOTime | optional | Planned start time of the task.                                                                                         |
| `planned_end_time`   | ISOTime | optional | Planned end time of the task.                                                                                           |
| `estimated_duration` | float   | optional | The estimated duration of the task.                                                                                     |
| `actual_start_time`  | ISOTime | optional | Actual start time of the task.                                                                                          |
| `actual_end_time`    | ISOTime | optional | Actual end time of the task.                                                                                            |
| `task_details`       | JSON    | optional | Additional use case specific data.                                                                                      |

## Process Data Structure

| Field             | Type         | Required | Description                                       |
| ----------------- | ------------ | -------- | ------------------------------------------------- |
| `id`              | string       | required | Process ID, in IOCS this is stored as `urn:<id>`  |
| `graph`           | JSON         | required | Task relationship, only Task IDs are stored here. |
| `current_events`  | string array | optional | Task IDs of running Tasks.                        |
| `process_details` | JSON         | optional | Additional Process information.                   |
| `series_id`       | string       | optional | Series ID of the Series the process belongs to.   |

A Directed Acyclic Graph (DAG) of task relationships is recorded as JSON, with only
the Task IDs stored in the `graph` field.

## Series Data Structure

| Field           | Type         | Required | Description                                                                                    |
| --------------- | ------------ | -------- | ---------------------------------------------------------------------------------------------- |
| `id`            | string       | required | Series ID, in IOCS this is stored as `urn:<id>`                                                |
| `type`          | string       | required | Series type, used to categorize the series (e.g., task or process series).                     |
| `cron`          | string       | required | Cron expression defining the recurrence schedule.                                              |
| `timezone`      | string       | required | Timezone for interpreting the cron expression and occurrence times.                            |
| `occurrences`   | string array | required | List of occurrences (linked task or process instances) belonging to this series.               |
| `until`         | ISOTime      | optional | End time for the series. If absent, the series recurs indefinitely.                            |
| `exception_ids` | string array | optional | IDs of occurrences marked as exceptions (e.g., skipped or individually rescheduled instances). |

Each `Occurrence` in the `occurrences` array contains a `time` (ISOTime) and an `id` (string) linking to its corresponding Task or Process.
