# Chefs Garden Fiji — Culinary Microgreens & Wholesale Platform

A modern Django + MySQL web platform designed for **Chefs Garden Fiji**, enabling Executive Chefs, Island Resorts, Fine-Dining Restaurants, and Superyachts across Fiji to browse culinary microgreens, inspect flavor profiles & dish pairings, and submit wholesale inquiries or tasting box requests.

## Quick Start (Docker Compose)

```bash
cd ~/Projects/chefs-garden-fiji
docker compose up -d --build
```

## Access URLs & Credentials

- **Public Chef's Catalog & Website**: [http://localhost:8080/](http://localhost:8080/)
- **Visual Product & Photo Studio**: [http://localhost:8080/manage/](http://localhost:8080/manage/)
- **Full Django Admin Panel**: [http://localhost:8080/admin/](http://localhost:8080/admin/)
  - **Username**: `admin`
  - **Password**: `chefsfiji2026`
- **MySQL Database (Host Port 3307)**:
  - **Database**: `chefs_garden_fiji`
  - **User**: `chef_user`
  - **Password**: `chef_pass_fiji`
