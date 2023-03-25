#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains the classes that represent Telegram InlineQueryResultMpeg4Gif."""
from typing import TYPE_CHECKING, Optional, Sequence, Tuple

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._messageentity import MessageEntity
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput
from telegram._utils.warnings_transition import (
    warn_about_deprecated_arg_return_new_arg,
    warn_about_deprecated_attr_in_property,
)
from telegram.constants import InlineQueryResultType

if TYPE_CHECKING:
    from telegram import InputMessageContent


class InlineQueryResultMpeg4Gif(InlineQueryResult):
    """
    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). By default, this
    animated MPEG-4 file will be sent by the user with optional caption. Alternatively, you can
    use :attr:`input_message_content` to send a message with the specified content instead of the
    animation.

    .. seealso:: :wiki:`Working with Files and Media <Working-with-Files-and-Media>`

    Args:
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        mpeg4_url (:obj:`str`): A valid URL for the MP4 file. File size must not exceed 1MB.
        mpeg4_width (:obj:`int`, optional): Video width.
        mpeg4_height (:obj:`int`, optional): Video height.
        mpeg4_duration (:obj:`int`, optional): Video duration in seconds.
        thumbnail_url (:obj:`str`, optional): URL of the static (JPEG or GIF) or animated (MPEG4)
            thumbnail for the result.

            Warning:
                The Bot API does **not** define this as an optional argument. It is formally
                optional for backwards compatibility with the deprecated :paramref:`thumb_url`.
                If you pass neither :paramref:`thumbnail_url` nor :paramref:`thumb_url`,
                :class:`ValueError` will be raised.

            .. versionadded:: NEXT.VERSION
        thumbnail_mime_type (:obj:`str`, optional): MIME type of the thumbnail, must be one of
            ``'image/jpeg'``, ``'image/gif'``, or ``'video/mp4'``. Defaults to ``'image/jpeg'``.

            .. versionadded:: NEXT.VERSION
        title (:obj:`str`, optional): Title for the result.
        caption (:obj:`str`, optional): Caption of the MPEG-4 file to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters
            after entities parsing.
        parse_mode (:obj:`str`, optional): |parse_mode|
        caption_entities (Sequence[:class:`telegram.MessageEntity`], optional):
            |captionentitiesattr|

            .. versionchanged:: 20.0
                |sequenceclassargs|

        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the video animation.

    Raises:
        :class:`ValueError`: If neither :paramref:`thumbnail_url` nor :paramref:`thumb_url` is
            supplied or if both are supplied and are not equal.

    Attributes:
        type (:obj:`str`): :tg-const:`telegram.constants.InlineQueryResultType.MPEG4GIF`.
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        mpeg4_url (:obj:`str`): A valid URL for the MP4 file. File size must not exceed 1MB.
        mpeg4_width (:obj:`int`): Optional. Video width.
        mpeg4_height (:obj:`int`): Optional. Video height.
        mpeg4_duration (:obj:`int`): Optional. Video duration in seconds.
        thumbnail_url (:obj:`str`): URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail
            for the result.

            .. versionadded:: NEXT.VERSION
        thumbnail_mime_type (:obj:`str`): Optional. MIME type of the thumbnail, must be one of
            ``'image/jpeg'``, ``'image/gif'``, or ``'video/mp4'``. Defaults to ``'image/jpeg'``.

            .. versionadded:: NEXT.VERSION
        title (:obj:`str`): Optional. Title for the result.
        caption (:obj:`str`): Optional. Caption of the MPEG-4 file to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters
            after entities parsing.
        parse_mode (:obj:`str`): Optional. |parse_mode|
        caption_entities (Tuple[:class:`telegram.MessageEntity`]): Optional. |caption_entities|

            .. versionchanged:: 20.0

                * |tupleclassattrs|
                * |alwaystuple|

        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional. Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`): Optional. Content of the
            message to be sent instead of the video animation.

    """

    __slots__ = (
        "reply_markup",
        "thumbnail_mime_type",
        "caption_entities",
        "mpeg4_duration",
        "mpeg4_width",
        "title",
        "caption",
        "parse_mode",
        "input_message_content",
        "mpeg4_url",
        "mpeg4_height",
        "thumbnail_url",
    )

    def __init__(
        self,
        id: str,  # pylint: disable=redefined-builtin
        mpeg4_url: str,
        # thumbnail_url is not optional in Telegram API, but we want to support thumb_url as well,
        # so thumbnail_url may not be passed.  We will raise ValueError manually if neither
        # thumbnail_url nor thumb_url are passed
        thumbnail_url: str = None,
        mpeg4_width: int = None,
        mpeg4_height: int = None,
        title: str = None,
        caption: str = None,
        reply_markup: InlineKeyboardMarkup = None,
        input_message_content: "InputMessageContent" = None,
        mpeg4_duration: int = None,
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        thumb_mime_type: str = None,
        caption_entities: Sequence[MessageEntity] = None,
        thumbnail_mime_type: str = None,
        # thumb_url is not optional in Telegram API, but it is here, along with thumbnail_url.
        thumb_url: str = None,
        *,
        api_kwargs: JSONDict = None,
    ):
        if not (thumbnail_url or thumb_url):
            raise ValueError(
                "You must pass either 'thumbnail_url' or 'thumb_url'. Note that 'thumb_url' is "
                "deprecated."
            )

        # Required
        super().__init__(InlineQueryResultType.MPEG4GIF, id, api_kwargs=api_kwargs)
        with self._unfrozen():
            self.mpeg4_url: str = mpeg4_url
            self.thumbnail_url: str = warn_about_deprecated_arg_return_new_arg(
                deprecated_arg=thumb_url,
                new_arg=thumbnail_url,
                deprecated_arg_name="thumb_url",
                new_arg_name="thumbnail_url",
                bot_api_version="6.6",
            )

            # Optional
            self.mpeg4_width: Optional[int] = mpeg4_width
            self.mpeg4_height: Optional[int] = mpeg4_height
            self.mpeg4_duration: Optional[int] = mpeg4_duration
            self.title: Optional[str] = title
            self.caption: Optional[str] = caption
            self.parse_mode: ODVInput[str] = parse_mode
            self.caption_entities: Tuple[MessageEntity, ...] = parse_sequence_arg(caption_entities)
            self.reply_markup: Optional[InlineKeyboardMarkup] = reply_markup
            self.input_message_content: Optional[InputMessageContent] = input_message_content
            self.thumbnail_mime_type: Optional[str] = warn_about_deprecated_arg_return_new_arg(
                deprecated_arg=thumb_mime_type,
                new_arg=thumbnail_mime_type,
                deprecated_arg_name="thumb_mime_type",
                new_arg_name="thumbnail_mime_type",
                bot_api_version="6.6",
            )

    @property
    def thumb_url(self) -> str:
        """:obj:`str`: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the
        result.

        .. deprecated:: NEXT.VERSION
           |thumbattributedeprecation| :attr:`thumbnail_url`.
        """
        warn_about_deprecated_attr_in_property(
            deprecated_attr_name="thumb_url",
            new_attr_name="thumbnail_url",
            bot_api_version="6.6",
        )
        return self.thumbnail_url

    @property
    def thumb_mime_type(self) -> Optional[str]:
        """:obj:`str`: Optional. Optional. MIME type of the thumbnail, must be one of
        ``'image/jpeg'``, ``'image/gif'``, or ``'video/mp4'``. Defaults to ``'image/jpeg'``.

        .. deprecated:: NEXT.VERSION
           |thumbattributedeprecation| :attr:`thumbnail_mime_type`.
        """
        warn_about_deprecated_attr_in_property(
            deprecated_attr_name="thumb_mime_type",
            new_attr_name="thumbnail_mime_type",
            bot_api_version="6.6",
        )
        return self.thumbnail_mime_type
