from ..db import Text
START_KB = {
    'categories':   Text.get_body(Text.START_KB_LIST_CATEGORYS),
    'discount':     Text.get_body(Text.START_KB_DISCOUNT),
    'news':         Text.get_body(Text.START_KB_NEWS)
    }

