from .config import LossConfig
from .model import Model

import chainer

from chainer import reporter


class Loss(chainer.link.Chain):
    def __init__(self, config: LossConfig, predictor: Model):
        super().__init__()
        self.config = config

        with self.init_scope():
            self.predictor = predictor

    def __call__(self, input, target, mask):
        input = chainer.as_variable(input)
        target = chainer.as_variable(target)
        mask = chainer.as_variable(mask)

        h = input
        y = self.predictor(h)

        loss = chainer.functions.sum(chainer.functions.absolute_error(y, target) * mask)
        loss = loss / chainer.functions.sum(mask)
        reporter.report({'loss': loss}, self)

        return loss * self.config.l1
