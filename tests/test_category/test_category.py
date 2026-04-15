from python_library.category.app_category import AppCategory
from python_library.category.category_action import CategoryAction
from python_library.category.category_group import CategoryGroup
from tests.test_category.enum_category import E_CATE, E_CATE_META_ELE


class TestCategory(AppCategory):
    def __init__(self) -> None:
        super().__init__()

    def register_category(self) -> None:
        self.cate_reg_queue[E_CATE.DOWNLOAD] = lambda: self.register_download()
        self.cate_reg_queue[E_CATE.UPLOAD] = lambda: self.register_upload()
        pass

    def register_download(self) -> None:
        download = CategoryGroup()

        document = CategoryGroup()
        image = CategoryGroup()
        video = CategoryGroup()

        # --- DOCUMENT ---
        document.push(
            E_CATE.E_DOWNLOAD.E_DOCUMENT.E_WORD[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_DOCUMENT.E_WORD[E_CATE_META_ELE.LAMBDA]),
        )
        document.push(
            E_CATE.E_DOWNLOAD.E_DOCUMENT.E_PDF[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_DOCUMENT.E_PDF[E_CATE_META_ELE.LAMBDA]),
        )
        document.push(
            E_CATE.E_DOWNLOAD.E_DOCUMENT.E_EXCEL[E_CATE_META_ELE.NAME],
            CategoryAction(
                E_CATE.E_DOWNLOAD.E_DOCUMENT.E_EXCEL[E_CATE_META_ELE.LAMBDA]
            ),
        )
        document.push(
            E_CATE.E_DOWNLOAD.E_DOCUMENT.E_TEXT[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_DOCUMENT.E_TEXT[E_CATE_META_ELE.LAMBDA]),
        )

        # --- IMAGE ---
        image.push(
            E_CATE.E_DOWNLOAD.E_IMAGE.E_JPEG[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_IMAGE.E_JPEG[E_CATE_META_ELE.LAMBDA]),
        )
        image.push(
            E_CATE.E_DOWNLOAD.E_IMAGE.E_PNG[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_IMAGE.E_PNG[E_CATE_META_ELE.LAMBDA]),
        )

        # --- VIDEO ---
        video.push(
            E_CATE.E_DOWNLOAD.E_VIDEO.E_MP4[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_VIDEO.E_MP4[E_CATE_META_ELE.LAMBDA]),
        )
        video.push(
            E_CATE.E_DOWNLOAD.E_VIDEO.E_AVI[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_VIDEO.E_AVI[E_CATE_META_ELE.LAMBDA]),
        )
        video.push(
            E_CATE.E_DOWNLOAD.E_VIDEO.E_MOV[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_DOWNLOAD.E_VIDEO.E_MOV[E_CATE_META_ELE.LAMBDA]),
        )

        # 최상위 DOWNLOAD 트리에 붙이기
        download.push(E_CATE.E_DOWNLOAD.DOCUMENT, document)
        download.push(E_CATE.E_DOWNLOAD.IMAGE, image)
        download.push(E_CATE.E_DOWNLOAD.VIDEO, video)

        self.cate_queue[E_CATE.DOWNLOAD] = download

    def register_upload(self) -> None:
        upload = CategoryGroup()

        document = CategoryGroup()
        image = CategoryGroup()
        video = CategoryGroup()

        # --- DOCUMENT ---
        document.push(
            E_CATE.E_UPLOAD.E_DOCUMENT.E_WORD[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_DOCUMENT.E_WORD[E_CATE_META_ELE.LAMBDA]),
        )
        document.push(
            E_CATE.E_UPLOAD.E_DOCUMENT.E_PDF[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_DOCUMENT.E_PDF[E_CATE_META_ELE.LAMBDA]),
        )
        document.push(
            E_CATE.E_UPLOAD.E_DOCUMENT.E_EXCEL[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_DOCUMENT.E_EXCEL[E_CATE_META_ELE.LAMBDA]),
        )
        document.push(
            E_CATE.E_UPLOAD.E_DOCUMENT.E_TEXT[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_DOCUMENT.E_TEXT[E_CATE_META_ELE.LAMBDA]),
        )

        # --- IMAGE ---
        image.push(
            E_CATE.E_UPLOAD.E_IMAGE.E_JPEG[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_IMAGE.E_JPEG[E_CATE_META_ELE.LAMBDA]),
        )
        image.push(
            E_CATE.E_UPLOAD.E_IMAGE.E_PNG[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_IMAGE.E_PNG[E_CATE_META_ELE.LAMBDA]),
        )

        # --- VIDEO ---
        video.push(
            E_CATE.E_UPLOAD.E_VIDEO.E_MP4[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_VIDEO.E_MP4[E_CATE_META_ELE.LAMBDA]),
        )
        video.push(
            E_CATE.E_UPLOAD.E_VIDEO.E_AVI[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_VIDEO.E_AVI[E_CATE_META_ELE.LAMBDA]),
        )
        video.push(
            E_CATE.E_UPLOAD.E_VIDEO.E_MOV[E_CATE_META_ELE.NAME],
            CategoryAction(E_CATE.E_UPLOAD.E_VIDEO.E_MOV[E_CATE_META_ELE.LAMBDA]),
        )

        # 최상위 DOWNLOAD 트리에 붙이기
        upload.push(E_CATE.E_UPLOAD.DOCUMENT, document)
        upload.push(E_CATE.E_UPLOAD.IMAGE, image)
        upload.push(E_CATE.E_UPLOAD.VIDEO, video)

        self.cate_queue[E_CATE.UPLOAD] = upload


def test_category():
    TestCategory.instance().get_cate_callback(E_CATE.DOWNLOAD)()
    TestCategory.instance().get_cate_callback(E_CATE.UPLOAD)()

    print()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

    print(TestCategory.instance().cate_queue)

    callback = (
        TestCategory.instance()
        .cate_queue[E_CATE.DOWNLOAD]
        .get(E_CATE.E_DOWNLOAD.VIDEO)
        .get(E_CATE.E_DOWNLOAD.E_VIDEO.MP4)
    )
    callback.invoke()

    download_group = TestCategory.instance().cate_queue[E_CATE.DOWNLOAD]
    all_actions = download_group.get_all_actions()
    print(all_actions)

    test = (
        TestCategory.instance().cate_queue[E_CATE.DOWNLOAD].get(E_CATE.E_DOWNLOAD.VIDEO)
    )
    video_actions = test.get_all_actions()
    print(video_actions)

    pass
