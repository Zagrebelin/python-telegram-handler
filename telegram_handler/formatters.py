import logging

from telegram_handler.utils import escape_html

__all__ = ['TelegramFormatter', 'MarkdownFormatter', 'HtmlFormatter']


class TelegramFormatter(logging.Formatter):
    """Base formatter class suitable for use with `TelegramHandler`"""

    fmt = "%(asctime)s %(levelname)s\n[%(name)s:%(funcName)s]\n%(message)s"
    parse_mode = None

    def __init__(self, fmt=None, *args, **kwargs):
        super(TelegramFormatter, self).__init__(fmt or self.fmt, *args, **kwargs)


class MarkdownFormatter(TelegramFormatter):
    """Markdown formatter for telegram."""
    fmt = '`%(asctime)s` *%(levelname)s*\n[%(name)s:%(funcName)s]\n%(message)s'
    parse_mode = 'Markdown'

    def formatException(self, *args, **kwargs):
        string = super(MarkdownFormatter, self).formatException(*args, **kwargs)
        return '```%s```' % string


class EMOJI:
    WHITE_CIRCLE = '\U000026AA'
    BLUE_CIRCLE = '\U0001F535'
    RED_CIRCLE = '\U0001F534'


class HtmlFormatter(TelegramFormatter):
    """HTML formatter for telegram."""
    fmt = '<code>%(asctime)s</code> <b>%(levelname)s</b>\nFrom %(name)s:%(funcName)s\n%(message)s'
    parse_mode = 'HTML'

    def __init__(self, *args, **kwargs):
        self.use_emoji = kwargs.pop('use_emoji', False)
        super(HtmlFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        """
        :param logging.LogRecord record:
        """
        super(HtmlFormatter, self).format(record)

        if record.funcName:
            record.funcName = escape_html(str(record.funcName))
        if record.name:
            record.name = escape_html(str(record.name))
        if record.msg:
            record.msg = escape_html(record.getMessage())
        if self.use_emoji:
            if record.levelno == logging.DEBUG:
                record.levelname += ' ' + EMOJI.WHITE_CIRCLE
            elif record.levelno == logging.INFO:
                record.levelname += ' ' + EMOJI.BLUE_CIRCLE
            else:
                record.levelname += ' ' + EMOJI.RED_CIRCLE

        return self.fmt % record.__dict__

    def formatException(self, *args, **kwargs):
        string = super(HtmlFormatter, self).formatException(*args, **kwargs)
        return '<pre>%s</pre>' % escape_html(string)
