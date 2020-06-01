class ParamData:
    def __init__(self, request, param, allowed, is_list=True, default=None):
        if is_list:
            args = self.sanitize_args(request, param, allowed.keys(), default)
            self.selected_args = args
            self.selected_labels = [allowed[arg] for arg in args]
        else:
            arg = self.sanitize_arg(request, param, allowed.keys(), default)
            self.selected_args = [arg]
            self.selected_labels = allowed[arg]
        self.choices = allowed

    @staticmethod
    def sanitize_arg(request, param, allowed, default=None):
        arg = request.GET.get(param, default)
        if arg not in allowed:
            arg = default
        return arg

    @staticmethod
    def sanitize_args(request, param, allowed, default=()):
        args = request.GET.getlist(param, default)
        if not all(arg in allowed for arg in args):
            args = default
        return set(args)

    @staticmethod
    def sanitize_int_arg(request, param, default=None):
        page = request.GET.get(param, default)
        try:
            return int(page)
        except ValueError:
            return default


class PagingData:
    def __init__(self, current_page, num_pages, num_records):
        self.current_page = current_page
        self.num_pages = num_pages
        self.num_records = num_records
        range_start = max(current_page - 2, 1)
        range_stop = min(range_start + 5, num_pages + 1)
        self.page_range = range(range_start, range_stop)

    def next_page(self):
        return self.current_page + 1

    def previous_page(self):
        return self.current_page - 1
