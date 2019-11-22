#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Record(object):
    def __init__(self):
        self.data = {}
        self.epochs = []

    def add(self, phase, metric, value, epoch):
        key = (phase, metric)
        if not key in self.data:
            self.data[key] = {}
        self.data[key][epoch] = value
        if epoch not in self.epochs:
            self.epochs.append(epoch)

    def add_phase(self, phase, results, epoch):
        for metric, value in results.items():
            self.add(phase, metric, value, epoch)

    def get_epoch(self, epoch, return_phases=None):
        _dict = { '/'.join(key): values[epoch]
            for key, values in self.data.items()
            if return_phases == None or key[0] in return_phases}
        return _dict

    def last_epoch(self):
        last_epoch = max(self.epochs)
        return last_epoch

    def last(self, return_phases=None):
        last_epoch = self.last_epoch()
        return self.get_epoch(last_epoch, return_phases=return_phases), last_epoch

    def best_epoch(self, phase, metric, reverse=False):
        best_epoch = sorted(self.data[(phase, metric)].items(), key=lambda x: x[1], reverse=reverse)[-1][0]
        return best_epoch

    def best(self, phase, metric, reverse=False, return_phases=None):
        best_epoch = self.best_epoch(phase, metric, reverse=reverse)
        return self.get_epoch(best_epoch, return_phases=return_phases), best_epoch


