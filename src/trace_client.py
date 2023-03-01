from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator, Optional, Union
from collections import namedtuple

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.span import SpanContext, TraceFlags, NonRecordingSpan
from opentelemetry.trace import set_span_in_context


TraceContext = namedtuple("TraceContext", ["trace_id", "span_id"])


def get_trace_context(trace: TraceClient) -> TraceContext:
    """Retrives span constext."""
    context = TraceContext(
        trace_id=trace.context.trace_id, span_id=trace.context.span_id
    )
    return context


def check_parent_context_validity(context: TraceContext) -> bool:
    """Checks span context validity."""
    res = True
    if context is not None:
        if not isinstance(context, TraceContext):
            res = False
        if not (
            (isinstance(context.trace_id, int))
            and (isinstance(context.span_id, int))
        ):
            res = False
    else:
        res = False
    return res


class TraceClient:

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Return cls instance if it exists."""
        if cls._instance is not None:
            return cls._instance
        instance = super(TraceClient, cls).__new__(cls)
        cls._instance = instance
        return cls._instance

    def __init__(
        self,
        service_name: Optional[str] = None,
        agent_host_name: Optional[str] = None,
        agent_port: Optional[int] = None,
        enabled: Optional[bool] = False,
    ):
        """Initialize TraceClient."""
        self._service_name = service_name
        self._agent_host_name = agent_host_name
        self._agent_port = agent_port
        self._enabled = enabled
        if "_tracer" not in self.__dict__:
            self._tracer = None
        self._init_tracer()

    def _init_tracer(self):
        """Initializes tracing exporter and span processor."""
        if not self._tracer:
            trace.set_tracer_provider(
                TracerProvider(
                    resource=Resource.create({SERVICE_NAME: self._service_name})
                )
            )
            jaeger_exporter = JaegerExporter(
                agent_host_name=self._agent_host_name,
                agent_port=self._agent_port,
            )
            trace.get_tracer_provider().add_span_processor(
                BatchSpanProcessor(jaeger_exporter)
            )

        self._tracer = trace.get_tracer(
            instrumenting_module_name=self._service_name,
        )

    @contextmanager
    def __call__(
        self, span_name: str, parent_context: TraceContext = None, **kwargs
    ) -> Union[Iterator[trace.Span], None]:
        """Context manager for span usage."""
        if self._enabled:
            if check_parent_context_validity(parent_context):
                span_context = SpanContext(
                    trace_id=parent_context.trace_id,
                    span_id=parent_context.span_id,
                    is_remote=True,
                    trace_flags=TraceFlags(0x01),
                )
                parent_context = set_span_in_context(
                    NonRecordingSpan(span_context)
                )
                with self._tracer.start_as_current_span(
                    span_name, context=parent_context
                ) as span:
                    if kwargs:
                        attributes = {
                            k: v for k, v in kwargs.items() if v is not None
                        }
                        span.set_attributes(attributes)
                    yield span
            else:
                with self._tracer.start_as_current_span(span_name) as span:
                    if kwargs:
                        attributes = {
                            k: v for k, v in kwargs.items() if v is not None
                        }
                        span.set_attributes(attributes)
                    yield span
        else:
            yield None
