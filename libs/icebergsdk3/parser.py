# -*- coding: utf-8 -*-

import urllib2, logging

logger = logging.getLogger('icebergsdk')


class XMLParser(object):
    path_to_products = "products.product"

    def parse_feed(self, feed_url):
        products = []

        try:
            file_down = urllib2.urlopen(feed_url, timeout=180)
        except urllib2.URLError, err:
            logger.error(err.read())

            if hasattr(err, 'reason'):
                logger.error(err.reason)
            else:
                logger.error(err)
        except urllib2.HTTPError, err:
            logger.error(err.read())

            if hasattr(err, 'reason'):
                logger.error(err.reason)
            else:
                logger.error(err)
        else:
            products = self.parse_file(file_down)

        # Close file
        try:
            file_down.close() # For sure, the two others maybe not
        except:
            pass

        return products

    def parse_file(self, the_file):
        """
        XML parsing using etree
        """
        from lxml import etree

        content = the_file.read()

        self.raw_dict = self.etree_to_dict(etree.fromstring(content).find("."))

        self.products_list = self.raw_dict
        for path in self.path_to_products.split("."):
            logger.debug("self.products_list keys=%s path=%s" % (self.products_list.keys(), path))
            self.products_list = self.products_list.get(path, {})

        return self.products_list


    def etree_to_dict(self, t, avoid_xml_double_dict=True):
        from collections import defaultdict
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self. etree_to_dict, children):
                for k, v in dc.iteritems():
                    dd[k].append(v)

            if not d.has_key(t.tag) or d[t.tag] == None:
                d[t.tag] = {}

            for k, v in dd.iteritems():
                if len(v) == 1:
                    real_v = v[0]
                    if avoid_xml_double_dict and type(real_v) == dict and len(real_v)==1 and k[:-1]==real_v.keys()[0]: ## "images":{"image":[image_array]} >> "images":[image_array]
                        real_v = real_v[real_v.keys()[0]]
                    d[t.tag][k] = real_v
                else:
                    d[t.tag][k] = v 
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d






