from page.models import Page, Tag


class PageService:
    @staticmethod
    def follow_unfollow(page, request) -> dict:
        if request.user not in page.followers.all():
            if page.is_private:
                page.follow_requests.add(request.user)
                msg = {'status': 'Follow request created'}

            else:
                page.followers.add(request.user)
                msg = {'status': 'Now you follow this page'}

        else:
            page.followers.remove(request.user)
            msg = {'status': 'You are no longer follow this page'}

        return msg

    @staticmethod
    def block_unblock(user_id: int, is_blocked: bool):
        pages = Page.objects.select_related('owner').filter(owner_id=user_id)
        for page in pages:
            if is_blocked and not page.is_blocked:
                page.is_blocked = True
            elif not is_blocked and page.is_blocked:
                page.is_blocked = False
            page.save()


class PostService:
    @staticmethod
    def like_unlike(post, request) -> dict:
        if request.user not in post.liked_by.all():
            post.liked_by.add(request.user)
            msg = {'status': 'You like this post'}

        else:
            post.liked_by.remove(request.user)
            msg = {'status': "You don't like this post anymore"}

        return msg


class TagService:
    @staticmethod
    def process_tags(request) -> list:
        tags_id = []
        if 'tags' in request.data:
            tags = request.data.pop('tags')
            existing_tags = Tag.objects.filter(name__in=tags)
            for tag in existing_tags:
                tags_id.append(tag.id)
                tags.remove(tag.name)
            for tag in tags:
                new_tag = Tag.objects.create(name=tag)
                new_tag.save()
                tags_id.append(new_tag.id)

        return tags_id