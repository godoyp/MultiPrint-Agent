import uuid
from multiprint_web_agent.core.agent_state import AGENT_STATE
from .zebra import print_zebra
from .laser import print_laser
from .renderer import render_to_images


def dispatch_print(printer: str, payload: dict):
    job_id = str(uuid.uuid4())

    AGENT_STATE.start_job(job_id)

    try:
        kind = payload.get("kind")

        if not kind:
            raise ValueError("Payload kind not specified")

        if kind == "zpl":
            print_zebra(printer, payload["raw"])
            AGENT_STATE.finish_job()
            return

        images = render_to_images(payload)
        print_laser(printer, images)
        AGENT_STATE.finish_job()

    except Exception as e:
        AGENT_STATE.fail_job(str(e))
        raise
