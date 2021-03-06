import pytest

from helpers.clickhouse import get_clickhouse_pod_spec
from helpers.utils import cleanup_helm, cleanup_k8s, install_chart, is_posthog_healthy, wait_for_pods_to_be_ready

VALUES_WITH_DIFFERENT_CLICKHOUSE_IMAGE = """
cloud: "local"

clickhouse:
  image:
    tag: 21.9.2.17
"""


@pytest.fixture(autouse=True)
def setup(kube):
    cleanup_k8s()
    cleanup_helm()
    install_chart(VALUES_WITH_DIFFERENT_CLICKHOUSE_IMAGE)
    wait_for_pods_to_be_ready(kube)


def test_posthog_healthy(kube):
    is_posthog_healthy(kube)


def test_clickhouse_pod_image(kube):
    pod_spec = get_clickhouse_pod_spec(kube)
    assert pod_spec.containers[0].image == "yandex/clickhouse-server:21.9.2.17"
