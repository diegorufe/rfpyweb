from rfpyweb.vo.rf_base_vo import RFBaseVo

"""
    Base class for audit changes
"""


class RFBaseAuditVo(RFBaseVo):

    def __init__(self):
        self.updatedAt = None
        self.createdAt = None
