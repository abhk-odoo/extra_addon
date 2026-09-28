# Method Performance

A small Odoo development tool to measure the performance of specific methods.

## What it does

The `@api.profile` decorator measures:

* Total execution time
* Python execution time
* Number of SQL queries
* SQL execution time
* SQL queries executed by the method

## Usage

Add `@api.profile` to the method you want to measure:

```python
from odoo import api, models


class PosSalesDetailReport(models.AbstractModel):
    _inherit = 'pos.sales.detail.report'

    @api.profile
    def _section_sales(self, *args, **kwargs):
        return super()._section_sales(*args, **kwargs)
```

## Output

The profiler prints results in the Odoo terminal:

```text
[METHOD PERFORMANCE]
Model        : pos.sales.detail.report
Method       : _section_sales
Total Time   : 8.16 ms
Python Time  : 5.23 ms
SQL Queries  : 4
SQL Time     : 2.92 ms

SQL QUERIES:

Query #1 (0.74 ms)
SELECT ...
```
