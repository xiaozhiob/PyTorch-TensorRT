import torch
import torch.nn as nn
from parameterized import parameterized
from torch.testing._internal.common_utils import run_tests

from .harness import DispatchTestCase


class TestNotEqualConverter(DispatchTestCase):
    @parameterized.expand(
        [
            ("2d", (5, 3)),
            ("3d", (5, 3, 2)),
        ]
    )
    def test_ne_tensor(self, _, shape):
        class ne(nn.Module):
            def forward(self, lhs_val, rhs_val):
                return torch.ops.aten.ne.Tensor(lhs_val, rhs_val)

        inputs = [
            torch.randint(0, 3, shape, dtype=torch.int32),
            torch.randint(0, 3, shape, dtype=torch.int32),
        ]
        self.run_test(
            ne(),
            inputs,
        )

    @parameterized.expand(
        [
            ("2d", (5, 3), 1),
            ("3d", (5, 3, 2), 2.0),
        ]
    )
    def test_ne_tensor_scalar(self, _, shape, scalar):
        class ne(nn.Module):
            def forward(self, lhs_val):
                return torch.ops.aten.ne.Tensor(lhs_val, torch.tensor(scalar))

        inputs = [torch.randint(0, 3, shape, dtype=torch.int32)]
        self.run_test(
            ne(),
            inputs,
        )

    @parameterized.expand(
        [
            ("2d", (5, 3), 1),
            ("3d", (5, 3, 2), 2.0),
        ]
    )
    def test_ne_scalar(self, _, shape, scalar):
        class ne(nn.Module):
            def forward(self, lhs_val):
                return torch.ops.aten.ne.Scalar(lhs_val, scalar)

        inputs = [torch.randint(0, 3, shape, dtype=torch.int32)]
        self.run_test(
            ne(),
            inputs,
        )


if __name__ == "__main__":
    run_tests()
