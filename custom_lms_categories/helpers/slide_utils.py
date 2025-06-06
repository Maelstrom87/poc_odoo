from odoo import fields

def get_cta_label(channel, partner_id):
    if is_user_subscribed_to_channel(channel, partner_id):
        return {
            "caption": "Continua",
            "color": "bg-green-600 hover:bg-green-500",
            "url": f"/slides/channel/{channel.id}"
        }
    else:
        return {
            "caption": "Vai al corso",
            "color": "bg-red-700 hover:bg-red-600",
            "url": channel.landing_url or "#"
        }

def is_user_subscribed_to_channel(channel, partner_id):
    return channel.env['slide.channel.partner'].sudo().search_count([
        ('partner_id', '=', partner_id),
        ('channel_id', '=', channel.id)
    ]) > 0

def get_course_ui_data(channel, partner_id=None):
    main_badge = channel.badge_ids.filtered(lambda b: b.main_badge)
    other_badges = channel.badge_ids.filtered(lambda b: not b.main_badge)

    return {
        "id": channel.id,
        "name": channel.name,
        "image": f"/web/image/slide.channel/{channel.id}/image_512" if channel.image_1920 else "/path/to/placeholder.jpg",
        "price": "€49.99",
        "total_slides": channel.total_slides,
        "total_time_hours": int(channel.total_time / 60) if channel.total_time else 0,
        "total_time_minutes": int(channel.total_time % 60) if channel.total_time else 0,
        "tags": channel.tag_ids.mapped('name'),
        "rating": round(channel.rating_avg or 4.7, 1),
        "is_new": channel.create_date and (fields.Datetime.now() - channel.create_date).days < 30,
        "main_badge": {
            "name": main_badge.name if main_badge else None,
            "color": main_badge.color if main_badge else None,
            "description": main_badge.description if main_badge else None,
        } if main_badge else None,
        "other_badges": [
            {
                "name": b.name,
                "color": b.color,
                "description": b.description
            } for b in other_badges
        ],
        "cta": get_cta_label(channel, partner_id) if partner_id else None,
        "card_hover_class": "hover:border-yellow-500",
        "icon_theme": "gold-on-black",
    }
