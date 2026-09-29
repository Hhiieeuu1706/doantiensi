# Online API and hardware-in-loop simulation test

Passed **11/11** tests.

- Median inference latency: 20.22 ms
- P95 latency: 34.95 ms
- Ensemble models: 10
- Replay source: NASA B0005 cycles 1–25

| Test | Passed | Detail |
|---|---:|---|
| health | True | {'status': 'ok', 'models': 10, 'protocol_id': 'battery-rul-protocol-v3.0'} |
| sequential_cycles | True | cycles 1..25 |
| state_buffer | True | 20 |
| physical_intervals | True | 25 cases |
| finite_latency | True | 25 cases |
| history_endpoint | True | 25 |
| invalid_payload_rejected | True | HTTP 400 expected |
| partial_cycle_endpoint | True | 119.519301948052 |
| idempotency | True | same response |
| concurrent_devices | True | 12 devices |
| reset | True | empty history |

This is software HIL/replay validation, not electrical hardware or a production BMS certification.
