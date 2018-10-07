# -*- coding: utf-8 -*-

import json
import codecs


class TengxunPipeline(object):
    def __init__(self):
        self.f = codecs.open('txzp.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.f.write(content)
        return item

    def spider_close(self, spider):
        self.f.close()
