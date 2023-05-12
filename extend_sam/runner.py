from datasets import Iterator
from .utils import Average_Meter, Timer, print_and_save_log
import torch

class BaseRunner():
    def __init__(self, model, optimizer, losses, train_loader, val_loader, scheduler):
        self.optimizer = optimizer
        self.losses = losses
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.model = model
        self.scheduler = scheduler
        self.train_timer = Timer()
        self.eval_timer = Timer()


class SemRunner(BaseRunner):
    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)

    def train(self, cfg):
        train_meter = Average_Meter(list(self.losses.keys()) + ['total_loss'])
        train_iterator = Iterator(self.train_loader)
        self.exist_status = ['train', 'eval', 'test']
        model_path = "{name.model_folder}/{name.experiment_name}/model.pth".format(name=cfg)
        writer = None
        if cfg.use_tensorboard is True:
            tensorborad_dir = "{name.tensorboard_folder}/{name.experiment_name}/tensorboard/".format(name=cfg)
            from torch.utils.tensorboard import SummaryWriter
            writer = SummaryWriter(tensorborad_dir)
        for iteration in range(cfg.max_iter):
            images, labels = train_iterator.get()
            images, labels = images.cuda(), labels.cuda()
            masks_pred, iou_pred = self.model(images)
            total_loss = None
            loss_dict = {}
            for index, item in enumerate(self.losses.items()):
                tmp_loss = item[1](masks_pred, labels)
                loss_dict[item[0]] = tmp_loss.item()
                total_loss += cfg.loss_weight[index] * tmp_loss

            self.optimizer.zero_grad()
            total_loss.backward()
            self.optimizer.step()
            self.scheduler.step()
            loss_dict['total_loss'] = total_loss.item()
            train_meter.add(loss_dict)

            if (iteration + 1) % cfg.log_iter == 0:
                self._write_log(cfg=cfg, train_meter=train_meter, status=self.exist_status[0], writer=writer)

            if (iteration + 1) % cfg.eval_iter == 0:
                self._eval()

    def _write_log(self, iteration, cfg, train_meter: Average_Meter, status, writer):
        log_data = train_meter.get(clear=True)
        log_data['iteration'] = iteration
        log_data['time'] = self.train_timer.end(clear=True)
        log_path = "{name.log_folder}/{name.experiment_name}/log_file.txt".format(name=cfg)
        message = "iteration : {val}, ".format(val=log_data['iteration'])
        for key, value in log_data.items():
            if key == 'iteration':
                continue
            message += "{key} : {val}, ".format(key=key, val=value)
        message = message[:-2] + '\n'
        print_and_save_log(message, log_path)
        # visualize
        if writer is not None:
            for key, value in log_data.items():
                writer.add_scalar("{status}/{key}".format(status=status, key=key), value, iteration)

    def test(self):
        pass

    def _eval(self):
        self.model.eval()
        self.eval_timer.tik()
        with torch.no_grad():
            for index, (images, labels) in enumerate(self.val_loader):
                pass

        self.model.train()
        pass
