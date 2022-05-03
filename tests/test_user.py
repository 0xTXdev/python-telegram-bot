#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2022
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
import pytest

from telegram import Update, User, Bot, InlineKeyboardButton
from telegram.helpers import escape_markdown
from tests.conftest import check_shortcut_signature, check_shortcut_call, check_defaults_handling


@pytest.fixture(scope='function')
def json_dict():
    return {
        'id': TestUser.id_,
        'is_bot': TestUser.is_bot,
        'first_name': TestUser.first_name,
        'last_name': TestUser.last_name,
        'username': TestUser.username,
        'language_code': TestUser.language_code,
        'can_join_groups': TestUser.can_join_groups,
        'can_read_all_group_messages': TestUser.can_read_all_group_messages,
        'supports_inline_queries': TestUser.supports_inline_queries,
    }


@pytest.fixture(scope='function')
def user(bot):
    return User(
        id=TestUser.id_,
        first_name=TestUser.first_name,
        is_bot=TestUser.is_bot,
        last_name=TestUser.last_name,
        username=TestUser.username,
        language_code=TestUser.language_code,
        can_join_groups=TestUser.can_join_groups,
        can_read_all_group_messages=TestUser.can_read_all_group_messages,
        supports_inline_queries=TestUser.supports_inline_queries,
        bot=bot,
    )


class TestUser:
    id_ = 1
    is_bot = True
    first_name = 'first\u2022name'
    last_name = 'last\u2022name'
    username = 'username'
    language_code = 'en_us'
    can_join_groups = True
    can_read_all_group_messages = True
    supports_inline_queries = False

    def test_slot_behaviour(self, user, mro_slots):
        for attr in user.__slots__:
            assert getattr(user, attr, 'err') != 'err', f"got extra slot '{attr}'"
        assert len(mro_slots(user)) == len(set(mro_slots(user))), "duplicate slot"

    def test_de_json(self, json_dict, bot):
        user = User.de_json(json_dict, bot)

        assert user.id == self.id_
        assert user.is_bot == self.is_bot
        assert user.first_name == self.first_name
        assert user.last_name == self.last_name
        assert user.username == self.username
        assert user.language_code == self.language_code
        assert user.can_join_groups == self.can_join_groups
        assert user.can_read_all_group_messages == self.can_read_all_group_messages
        assert user.supports_inline_queries == self.supports_inline_queries

    def test_de_json_without_username(self, json_dict, bot):
        del json_dict['username']

        user = User.de_json(json_dict, bot)

        assert user.id == self.id_
        assert user.is_bot == self.is_bot
        assert user.first_name == self.first_name
        assert user.last_name == self.last_name
        assert user.username is None
        assert user.language_code == self.language_code
        assert user.can_join_groups == self.can_join_groups
        assert user.can_read_all_group_messages == self.can_read_all_group_messages
        assert user.supports_inline_queries == self.supports_inline_queries

    def test_de_json_without_username_and_last_name(self, json_dict, bot):
        del json_dict['username']
        del json_dict['last_name']

        user = User.de_json(json_dict, bot)

        assert user.id == self.id_
        assert user.is_bot == self.is_bot
        assert user.first_name == self.first_name
        assert user.last_name is None
        assert user.username is None
        assert user.language_code == self.language_code
        assert user.can_join_groups == self.can_join_groups
        assert user.can_read_all_group_messages == self.can_read_all_group_messages
        assert user.supports_inline_queries == self.supports_inline_queries

    def test_name(self, user):
        assert user.name == '@username'
        user.username = None
        assert user.name == 'first\u2022name last\u2022name'
        user.last_name = None
        assert user.name == 'first\u2022name'
        user.username = self.username
        assert user.name == '@username'

    def test_full_name(self, user):
        assert user.full_name == 'first\u2022name last\u2022name'
        user.last_name = None
        assert user.full_name == 'first\u2022name'

    def test_link(self, user):
        assert user.link == f'https://t.me/{user.username}'
        user.username = None
        assert user.link is None

    @pytest.mark.asyncio
    async def test_instance_method_get_profile_photos(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['user_id'] == user.id

        assert check_shortcut_signature(
            User.get_profile_photos, Bot.get_user_profile_photos, ['user_id'], []
        )
        assert await check_shortcut_call(
            user.get_profile_photos, user.get_bot(), 'get_user_profile_photos'
        )
        assert await check_defaults_handling(user.get_profile_photos, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'get_user_profile_photos', make_assertion)
        assert await user.get_profile_photos()

    @pytest.mark.asyncio
    async def test_instance_method_pin_message(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id

        assert check_shortcut_signature(User.pin_message, Bot.pin_chat_message, ['chat_id'], [])
        assert await check_shortcut_call(user.pin_message, user.get_bot(), 'pin_chat_message')
        assert await check_defaults_handling(user.pin_message, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'pin_chat_message', make_assertion)
        assert await user.pin_message(1)

    @pytest.mark.asyncio
    async def test_instance_method_unpin_message(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id

        assert check_shortcut_signature(
            User.unpin_message, Bot.unpin_chat_message, ['chat_id'], []
        )
        assert await check_shortcut_call(user.unpin_message, user.get_bot(), 'unpin_chat_message')
        assert await check_defaults_handling(user.unpin_message, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'unpin_chat_message', make_assertion)
        assert await user.unpin_message()

    @pytest.mark.asyncio
    async def test_instance_method_unpin_all_messages(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id

        assert check_shortcut_signature(
            User.unpin_all_messages, Bot.unpin_all_chat_messages, ['chat_id'], []
        )
        assert await check_shortcut_call(
            user.unpin_all_messages, user.get_bot(), 'unpin_all_chat_messages'
        )
        assert await check_defaults_handling(user.unpin_all_messages, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'unpin_all_chat_messages', make_assertion)
        assert await user.unpin_all_messages()

    @pytest.mark.asyncio
    async def test_instance_method_send_message(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['text'] == 'test'

        assert check_shortcut_signature(User.send_message, Bot.send_message, ['chat_id'], [])
        assert await check_shortcut_call(user.send_message, user.get_bot(), 'send_message')
        assert await check_defaults_handling(user.send_message, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_message', make_assertion)
        assert await user.send_message('test')

    @pytest.mark.asyncio
    async def test_instance_method_send_photo(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['photo'] == 'test_photo'

        assert check_shortcut_signature(User.send_photo, Bot.send_photo, ['chat_id'], [])
        assert await check_shortcut_call(user.send_photo, user.get_bot(), 'send_photo')
        assert await check_defaults_handling(user.send_photo, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_photo', make_assertion)
        assert await user.send_photo('test_photo')

    @pytest.mark.asyncio
    async def test_instance_method_send_media_group(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['media'] == 'test_media_group'

        assert check_shortcut_signature(
            User.send_media_group, Bot.send_media_group, ['chat_id'], []
        )
        assert await check_shortcut_call(user.send_media_group, user.get_bot(), 'send_media_group')
        assert await check_defaults_handling(user.send_media_group, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_media_group', make_assertion)
        assert await user.send_media_group('test_media_group')

    @pytest.mark.asyncio
    async def test_instance_method_send_audio(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['audio'] == 'test_audio'

        assert check_shortcut_signature(User.send_audio, Bot.send_audio, ['chat_id'], [])
        assert await check_shortcut_call(user.send_audio, user.get_bot(), 'send_audio')
        assert await check_defaults_handling(user.send_audio, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_audio', make_assertion)
        assert await user.send_audio('test_audio')

    @pytest.mark.asyncio
    async def test_instance_method_send_chat_action(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['action'] == 'test_chat_action'

        assert check_shortcut_signature(
            User.send_chat_action, Bot.send_chat_action, ['chat_id'], []
        )
        assert await check_shortcut_call(user.send_chat_action, user.get_bot(), 'send_chat_action')
        assert await check_defaults_handling(user.send_chat_action, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_chat_action', make_assertion)
        assert await user.send_chat_action('test_chat_action')

    @pytest.mark.asyncio
    async def test_instance_method_send_contact(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['phone_number'] == 'test_contact'

        assert check_shortcut_signature(User.send_contact, Bot.send_contact, ['chat_id'], [])
        assert await check_shortcut_call(user.send_contact, user.get_bot(), 'send_contact')
        assert await check_defaults_handling(user.send_contact, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_contact', make_assertion)
        assert await user.send_contact(phone_number='test_contact')

    @pytest.mark.asyncio
    async def test_instance_method_send_dice(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['emoji'] == 'test_dice'

        assert check_shortcut_signature(User.send_dice, Bot.send_dice, ['chat_id'], [])
        assert await check_shortcut_call(user.send_dice, user.get_bot(), 'send_dice')
        assert await check_defaults_handling(user.send_dice, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_dice', make_assertion)
        assert await user.send_dice(emoji='test_dice')

    @pytest.mark.asyncio
    async def test_instance_method_send_document(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['document'] == 'test_document'

        assert check_shortcut_signature(User.send_document, Bot.send_document, ['chat_id'], [])
        assert await check_shortcut_call(user.send_document, user.get_bot(), 'send_document')
        assert await check_defaults_handling(user.send_document, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_document', make_assertion)
        assert await user.send_document('test_document')

    @pytest.mark.asyncio
    async def test_instance_method_send_game(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['game_short_name'] == 'test_game'

        assert check_shortcut_signature(User.send_game, Bot.send_game, ['chat_id'], [])
        assert await check_shortcut_call(user.send_game, user.get_bot(), 'send_game')
        assert await check_defaults_handling(user.send_game, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_game', make_assertion)
        assert await user.send_game(game_short_name='test_game')

    @pytest.mark.asyncio
    async def test_instance_method_send_invoice(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            title = kwargs['title'] == 'title'
            description = kwargs['description'] == 'description'
            payload = kwargs['payload'] == 'payload'
            provider_token = kwargs['provider_token'] == 'provider_token'
            currency = kwargs['currency'] == 'currency'
            prices = kwargs['prices'] == 'prices'
            args = title and description and payload and provider_token and currency and prices
            return kwargs['chat_id'] == user.id and args

        assert check_shortcut_signature(User.send_invoice, Bot.send_invoice, ['chat_id'], [])
        assert await check_shortcut_call(user.send_invoice, user.get_bot(), 'send_invoice')
        assert await check_defaults_handling(user.send_invoice, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_invoice', make_assertion)
        assert await user.send_invoice(
            'title',
            'description',
            'payload',
            'provider_token',
            'currency',
            'prices',
        )

    @pytest.mark.asyncio
    async def test_instance_method_send_location(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['latitude'] == 'test_location'

        assert check_shortcut_signature(User.send_location, Bot.send_location, ['chat_id'], [])
        assert await check_shortcut_call(user.send_location, user.get_bot(), 'send_location')
        assert await check_defaults_handling(user.send_location, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_location', make_assertion)
        assert await user.send_location('test_location')

    @pytest.mark.asyncio
    async def test_instance_method_send_sticker(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['sticker'] == 'test_sticker'

        assert check_shortcut_signature(User.send_sticker, Bot.send_sticker, ['chat_id'], [])
        assert await check_shortcut_call(user.send_sticker, user.get_bot(), 'send_sticker')
        assert await check_defaults_handling(user.send_sticker, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_sticker', make_assertion)
        assert await user.send_sticker('test_sticker')

    @pytest.mark.asyncio
    async def test_instance_method_send_video(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['video'] == 'test_video'

        assert check_shortcut_signature(User.send_video, Bot.send_video, ['chat_id'], [])
        assert await check_shortcut_call(user.send_video, user.get_bot(), 'send_video')
        assert await check_defaults_handling(user.send_video, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_video', make_assertion)
        assert await user.send_video('test_video')

    @pytest.mark.asyncio
    async def test_instance_method_send_venue(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['title'] == 'test_venue'

        assert check_shortcut_signature(User.send_venue, Bot.send_venue, ['chat_id'], [])
        assert await check_shortcut_call(user.send_venue, user.get_bot(), 'send_venue')
        assert await check_defaults_handling(user.send_venue, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_venue', make_assertion)
        assert await user.send_venue(title='test_venue')

    @pytest.mark.asyncio
    async def test_instance_method_send_video_note(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['video_note'] == 'test_video_note'

        assert check_shortcut_signature(User.send_video_note, Bot.send_video_note, ['chat_id'], [])
        assert await check_shortcut_call(user.send_video_note, user.get_bot(), 'send_video_note')
        assert await check_defaults_handling(user.send_video_note, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_video_note', make_assertion)
        assert await user.send_video_note('test_video_note')

    @pytest.mark.asyncio
    async def test_instance_method_send_voice(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['voice'] == 'test_voice'

        assert check_shortcut_signature(User.send_voice, Bot.send_voice, ['chat_id'], [])
        assert await check_shortcut_call(user.send_voice, user.get_bot(), 'send_voice')
        assert await check_defaults_handling(user.send_voice, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_voice', make_assertion)
        assert await user.send_voice('test_voice')

    @pytest.mark.asyncio
    async def test_instance_method_send_animation(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['animation'] == 'test_animation'

        assert check_shortcut_signature(User.send_animation, Bot.send_animation, ['chat_id'], [])
        assert await check_shortcut_call(user.send_animation, user.get_bot(), 'send_animation')
        assert await check_defaults_handling(user.send_animation, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_animation', make_assertion)
        assert await user.send_animation('test_animation')

    @pytest.mark.asyncio
    async def test_instance_method_send_poll(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['question'] == 'test_poll'

        assert check_shortcut_signature(User.send_poll, Bot.send_poll, ['chat_id'], [])
        assert await check_shortcut_call(user.send_poll, user.get_bot(), 'send_poll')
        assert await check_defaults_handling(user.send_poll, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'send_poll', make_assertion)
        assert await user.send_poll(question='test_poll', options=[1, 2])

    @pytest.mark.asyncio
    async def test_instance_method_send_copy(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            user_id = kwargs['chat_id'] == user.id
            message_id = kwargs['message_id'] == 'message_id'
            from_chat_id = kwargs['from_chat_id'] == 'from_chat_id'
            return from_chat_id and message_id and user_id

        assert check_shortcut_signature(User.send_copy, Bot.copy_message, ['chat_id'], [])
        assert await check_shortcut_call(user.copy_message, user.get_bot(), 'copy_message')
        assert await check_defaults_handling(user.copy_message, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'copy_message', make_assertion)
        assert await user.send_copy(from_chat_id='from_chat_id', message_id='message_id')

    @pytest.mark.asyncio
    async def test_instance_method_copy_message(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            chat_id = kwargs['chat_id'] == 'chat_id'
            message_id = kwargs['message_id'] == 'message_id'
            user_id = kwargs['from_chat_id'] == user.id
            return chat_id and message_id and user_id

        assert check_shortcut_signature(User.copy_message, Bot.copy_message, ['from_chat_id'], [])
        assert await check_shortcut_call(user.copy_message, user.get_bot(), 'copy_message')
        assert await check_defaults_handling(user.copy_message, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'copy_message', make_assertion)
        assert await user.copy_message(chat_id='chat_id', message_id='message_id')

    @pytest.mark.asyncio
    async def test_instance_method_get_menu_button(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id

        assert check_shortcut_signature(
            User.get_menu_button, Bot.get_chat_menu_button, ['chat_id'], []
        )
        assert await check_shortcut_call(
            user.get_menu_button,
            user.get_bot(),
            'get_chat_menu_button',
            shortcut_kwargs=['chat_id'],
        )
        assert await check_defaults_handling(user.get_menu_button, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'get_chat_menu_button', make_assertion)
        assert await user.get_menu_button()

    @pytest.mark.asyncio
    async def test_instance_method_set_menu_button(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            return kwargs['chat_id'] == user.id and kwargs['menu_button'] == 'menu_button'

        assert check_shortcut_signature(
            User.set_menu_button, Bot.set_chat_menu_button, ['chat_id'], []
        )
        assert await check_shortcut_call(
            user.set_menu_button,
            user.get_bot(),
            'set_chat_menu_button',
            shortcut_kwargs=['chat_id'],
        )
        assert await check_defaults_handling(user.set_menu_button, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'set_chat_menu_button', make_assertion)
        assert await user.set_menu_button(menu_button='menu_button')

    @pytest.mark.asyncio
    async def test_instance_method_approve_join_request(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            chat_id = kwargs['chat_id'] == 'chat_id'
            user_id = kwargs['user_id'] == user.id
            return chat_id and user_id

        assert check_shortcut_signature(
            User.approve_join_request, Bot.approve_chat_join_request, ['user_id'], []
        )
        assert await check_shortcut_call(
            user.approve_join_request, user.get_bot(), 'approve_chat_join_request'
        )
        assert await check_defaults_handling(user.approve_join_request, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'approve_chat_join_request', make_assertion)
        assert await user.approve_join_request(chat_id='chat_id')

    @pytest.mark.asyncio
    async def test_instance_method_decline_join_request(self, monkeypatch, user):
        async def make_assertion(*_, **kwargs):
            chat_id = kwargs['chat_id'] == 'chat_id'
            user_id = kwargs['user_id'] == user.id
            return chat_id and user_id

        assert check_shortcut_signature(
            User.decline_join_request, Bot.decline_chat_join_request, ['user_id'], []
        )
        assert await check_shortcut_call(
            user.decline_join_request, user.get_bot(), 'decline_chat_join_request'
        )
        assert await check_defaults_handling(user.decline_join_request, user.get_bot())

        monkeypatch.setattr(user.get_bot(), 'decline_chat_join_request', make_assertion)
        assert await user.decline_join_request(chat_id='chat_id')

    @pytest.mark.asyncio
    async def test_mention_html(self, user):
        expected = '<a href="tg://user?id={}">{}</a>'

        assert user.mention_html() == expected.format(user.id, user.full_name)
        assert user.mention_html('the<b>name\u2022') == expected.format(
            user.id, 'the&lt;b&gt;name\u2022'
        )
        assert user.mention_html(user.username) == expected.format(user.id, user.username)

    def test_mention_button(self, user):
        expected_name = InlineKeyboardButton(text="Bob", url=f"tg://user?id={user.id}")
        expected_full = InlineKeyboardButton(text=user.full_name, url=f"tg://user?id={user.id}")

        assert user.mention_button("Bob") == expected_name
        assert user.mention_button() == expected_full

    def test_mention_markdown(self, user):
        expected = '[{}](tg://user?id={})'

        assert user.mention_markdown() == expected.format(user.full_name, user.id)
        assert user.mention_markdown('the_name*\u2022') == expected.format(
            'the\\_name\\*\u2022', user.id
        )
        assert user.mention_markdown(user.username) == expected.format(user.username, user.id)

    @pytest.mark.asyncio
    async def test_mention_markdown_v2(self, user):
        user.first_name = 'first{name'
        user.last_name = 'last_name'

        expected = '[{}](tg://user?id={})'

        assert user.mention_markdown_v2() == expected.format(
            escape_markdown(user.full_name, version=2), user.id
        )
        assert user.mention_markdown_v2('the{name>\u2022') == expected.format(
            'the\\{name\\>\u2022', user.id
        )
        assert user.mention_markdown_v2(user.username) == expected.format(user.username, user.id)

    def test_equality(self):
        a = User(self.id_, self.first_name, self.is_bot, self.last_name)
        b = User(self.id_, self.first_name, self.is_bot, self.last_name)
        c = User(self.id_, self.first_name, self.is_bot)
        d = User(0, self.first_name, self.is_bot, self.last_name)
        e = Update(self.id_)

        assert a == b
        assert hash(a) == hash(b)
        assert a is not b

        assert a == c
        assert hash(a) == hash(c)

        assert a != d
        assert hash(a) != hash(d)

        assert a != e
        assert hash(a) != hash(e)
