# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('stories_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['stories.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('stories', ['Category'])

        # Adding model 'Story'
        db.create_table('stories_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['stories.Category'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('registration_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('karma', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('digs_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('buries_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('comments_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('stories', ['Story'])

        # Adding model 'StoryFlag'
        db.create_table('story_flags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='story_flags', to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='flags', to=orm['stories.Story'])),
            ('flag', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
            ('flag_date', self.gf('django.db.models.fields.DateTimeField')(default=None)),
        ))
        db.send_create_signal('stories', ['StoryFlag'])

        # Adding unique constraint on 'StoryFlag', fields ['user', 'story', 'flag']
        db.create_unique('story_flags', ['user_id', 'story_id', 'flag'])

        # Adding model 'UserPref'
        db.create_table('stories_userpref', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='pref', unique=True, to=orm['auth.User'])),
            ('comment_threshold', self.gf('django.db.models.fields.SmallIntegerField')(default=-10)),
            ('comment_rating_style', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('frame', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('upcoming_sort', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('popular_sort', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
        ))
        db.send_create_signal('stories', ['UserPref'])

        # Adding model 'Reference'
        db.create_table('stories_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='references', to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='references', to=orm['stories.Story'])),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_removed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('stories', ['Reference'])

        # Adding model 'Watch'
        db.create_table('stories_watch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('stories', ['Watch'])

        # Adding unique constraint on 'Watch', fields ['user', 'story']
        db.create_unique('stories_watch', ['user_id', 'story_id'])

        # Adding model 'Save'
        db.create_table('stories_save', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Story'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('stories', ['Save'])

        # Adding unique constraint on 'Save', fields ['user', 'story']
        db.create_unique('stories_save', ['user_id', 'story_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Save', fields ['user', 'story']
        db.delete_unique('stories_save', ['user_id', 'story_id'])

        # Removing unique constraint on 'Watch', fields ['user', 'story']
        db.delete_unique('stories_watch', ['user_id', 'story_id'])

        # Removing unique constraint on 'StoryFlag', fields ['user', 'story', 'flag']
        db.delete_unique('story_flags', ['user_id', 'story_id', 'flag'])

        # Deleting model 'Category'
        db.delete_table('stories_category')

        # Deleting model 'Story'
        db.delete_table('stories_story')

        # Deleting model 'StoryFlag'
        db.delete_table('story_flags')

        # Deleting model 'UserPref'
        db.delete_table('stories_userpref')

        # Deleting model 'Reference'
        db.delete_table('stories_reference')

        # Deleting model 'Watch'
        db.delete_table('stories_watch')

        # Deleting model 'Save'
        db.delete_table('stories_save')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': "orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'stories.category': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['stories.Category']"}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'stories.reference': {
            'Meta': {'ordering': "('created_date',)", 'object_name': 'Reference'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'references'", 'to': "orm['stories.Story']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'references'", 'to': "orm['auth.User']"})
        },
        'stories.save': {
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'Save'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'stories.story': {
            'Meta': {'ordering': "('published_date',)", 'object_name': 'Story'},
            'buries_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['stories.Category']"}),
            'comments_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'digs_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'karma': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saved': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'saved'", 'to': "orm['auth.User']", 'through': "orm['stories.Save']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['auth.User']"}),
            'watched': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'watched'", 'to': "orm['auth.User']", 'through': "orm['stories.Watch']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'})
        },
        'stories.storyflag': {
            'Meta': {'unique_together': "[('user', 'story', 'flag')]", 'object_name': 'StoryFlag', 'db_table': "'story_flags'"},
            'flag': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'flag_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flags'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_flags'", 'to': "orm['auth.User']"})
        },
        'stories.userpref': {
            'Meta': {'object_name': 'UserPref'},
            'comment_rating_style': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_threshold': ('django.db.models.fields.SmallIntegerField', [], {'default': '-10'}),
            'frame': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'popular_sort': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'upcoming_sort': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'pref'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'stories.watch': {
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'Watch'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'voting.vote': {
            'Meta': {'unique_together': "(('user', 'content_type', 'object_id'),)", 'object_name': 'Vote', 'db_table': "'votes'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'reason': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {})
        }
    }

    complete_apps = ['stories']
