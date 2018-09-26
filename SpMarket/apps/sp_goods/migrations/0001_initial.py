# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-25 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('title', models.CharField(max_length=150, verbose_name='活动名称')),
                ('img_url', models.ImageField(upload_to='activity/%Y%m/%d', verbose_name='活动图片地址')),
                ('url_site', models.CharField(max_length=200, verbose_name='活动的url地址')),
            ],
            options={
                'verbose_name': '活动管理',
                'verbose_name_plural': '活动管理',
            },
        ),
        migrations.CreateModel(
            name='ActivityZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('title', models.CharField(max_length=150, verbose_name='活动专区名称')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='活动专区的简介')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_on_sale', models.BooleanField(choices=[(0, '下架'), (1, '上架')], default=0, verbose_name='上否上线')),
            ],
            options={
                'verbose_name': '活动专区管理',
                'verbose_name_plural': '活动专区管理',
            },
        ),
        migrations.CreateModel(
            name='ActivityZoneGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('activity_zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.ActivityZone', verbose_name='活动专区ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=150, verbose_name='轮播活动名')),
                ('img_url', models.ImageField(upload_to='banner/%Y%m/%d', verbose_name='轮播图片地址')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '首页轮播管理',
                'verbose_name_plural': '首页轮播管理',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('cate_name', models.CharField(max_length=20, verbose_name='分类名称')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '商品分类管理',
                'verbose_name_plural': '商品分类管理',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('img_url', models.ImageField(upload_to='goods_gallery/%Y%m/%d', verbose_name='相册图片地址')),
            ],
            options={
                'verbose_name': '商品相册管理',
                'verbose_name_plural': '商品相册管理',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('sku_name', models.CharField(max_length=100, verbose_name='商品SKU名称')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='商品的简介')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='价格')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('sale_num', models.IntegerField(default=0, verbose_name='销量')),
                ('logo', models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='封面图片')),
                ('is_on_sale', models.BooleanField(choices=[(0, '下架'), (1, '上架')], default=0, verbose_name='是否上架')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.Category', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': '商品管理',
                'verbose_name_plural': '商品管理',
            },
        ),
        migrations.CreateModel(
            name='GoodsSPU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('spu_name', models.CharField(max_length=20, verbose_name='商品SPU名称')),
                ('content', models.TextField(verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(max_length=20, verbose_name='单位')),
            ],
            options={
                'verbose_name': '商品单位管理',
                'verbose_name_plural': '商品单位管理',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goods_spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.GoodsSPU', verbose_name='商品SPU'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.Unit', verbose_name='单位'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='goods_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.GoodsSKU', verbose_name='SKU商品'),
        ),
        migrations.AddField(
            model_name='banner',
            name='goods_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.GoodsSKU', verbose_name='SKU商品'),
        ),
        migrations.AddField(
            model_name='activityzonegoods',
            name='goods_sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sp_goods.GoodsSKU', verbose_name='专区商品SKU_ID'),
        ),
    ]
