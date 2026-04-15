from python_library.define.enum import IENUM


class E_CATE_META_ELE(IENUM):
    NAME = 0
    LAMBDA = 1


class E_CATE(IENUM):
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"

    class E_DOWNLOAD(IENUM):
        DOCUMENT = "DOCUMENT"
        IMAGE = "IMAGE"
        VIDEO = "VIDEO"

        class E_DOCUMENT(IENUM):
            WORD = "WORD"
            E_WORD = (WORD, lambda: print("WORD"))
            PDF = "PDF"
            E_PDF = (PDF, lambda: print("PDF"))
            EXCEL = "EXCEL"
            E_EXCEL = (EXCEL, lambda: print("EXCEL"))
            TEXT = "TEXT"
            E_TEXT = (TEXT, lambda: print("TEXT"))

        class E_IMAGE(IENUM):
            JPEG = "JPEG"
            E_JPEG = (JPEG, lambda: print("JPEG"))
            PNG = "PNG"
            E_PNG = (PNG, lambda: print("PNG"))

        class E_VIDEO(IENUM):
            MP4 = "MP4"
            E_MP4 = (MP4, lambda: print("MP4"))
            AVI = "AVI"
            E_AVI = (AVI, lambda: print("AVI"))
            MOV = "MOV"
            E_MOV = (MOV, lambda: print("MOV"))

    class E_UPLOAD(IENUM):
        DOCUMENT = "DOCUMENT"
        IMAGE = "IMAGE"
        VIDEO = "VIDEO"

        class E_DOCUMENT(IENUM):
            WORD = "WORD"
            E_WORD = (WORD, lambda: print("WORD"))
            PDF = "PDF"
            E_PDF = (PDF, lambda: print("PDF"))
            EXCEL = "EXCEL"
            E_EXCEL = (EXCEL, lambda: print("EXCEL"))
            TEXT = "TEXT"
            E_TEXT = (TEXT, lambda: print("TEXT"))

        class E_IMAGE(IENUM):
            JPEG = "JPEG"
            E_JPEG = (JPEG, lambda: print("JPEG"))
            PNG = "PNG"
            E_PNG = (PNG, lambda: print("PNG"))

        class E_VIDEO(IENUM):
            MP4 = "MP4"
            E_MP4 = (MP4, lambda: print("MP4"))
            AVI = "AVI"
            E_AVI = (AVI, lambda: print("AVI"))
            MOV = "MOV"
            E_MOV = (MOV, lambda: print("MOV"))
