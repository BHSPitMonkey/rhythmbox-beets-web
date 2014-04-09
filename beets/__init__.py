'''Beets Web plugin for Rhythmbox

API information: http://beets.readthedocs.org/en/latest/plugins/web.html

Be sure to edit BEETS_WEB_URL to the correct URL for your Beets web app!

Wish list:
	- Preferences UI for adding/removing Beets Web hosts (currently hardcoded)
	- Progress UI while fetching list
	- Stream the JSON->Entry process as data comes in instead of all at the end
	- Source icon (PNG already included, just haven't written supporting code yet)
'''
import json

from gi.repository import GObject, Peas, RB
import rb


BEETS_WEB_URL = "http://192.168.1.101:8337"  # TODO: Don't hardcode

class BeetsWebPlugin (GObject.Object, Peas.Activatable):
	object = GObject.Property(type=GObject.Object)
	def __init__(self):
		super(BeetsWebPlugin, self).__init__()

	def do_activate(self):
		print("Plugin activated")
		
		shell = self.object
		db = shell.props.db
		entry_type = BeetsEntryType()
		db.register_entry_type(entry_type)
		source = GObject.new(
			BeetsSource,
			shell=shell,
			name=_("Beets Library"),
			entry_type=entry_type,
		)
		group = RB.DisplayPageGroup.get_by_id ("library")
		shell.append_display_page (source, group)
		shell.register_entry_type_for_source(source, entry_type)

class BeetsEntryType(RB.RhythmDBEntryType):
	def __init__(self):
		RB.RhythmDBEntryType.__init__(self, name='beets-entry-type')

class BeetsSource(RB.BrowserSource):
	__activated=False
	__base_url=BEETS_WEB_URL

	def __init__(self):
		RB.BrowserSource.__init__(self)

		self.__activated = False
		self.__shell = None
		self.__db = None
		self.__entry_type = None

	def do_selected(self):
		'''Called when source is selected in sidebar'''
		if not self.__activated:  # Only runs the first time
			self.__shell = self.props.shell
			self.__db = self.__shell.props.db
			self.__entry_type = self.props.entry_type

			self.__activated = True

			# Connect to Beets and fetch the song list
			beets_items_url = "%s/item/" % self.__base_url
			loader = rb.Loader()
			loader.get_url(beets_items_url, self.on_beets_items_downloaded)            

	def on_beets_items_downloaded(self, data):
		'''Processes downloaded song list'''
		songlist = json.loads(data.decode('utf8'))
		for item in songlist['items']:
			entry = RB.RhythmDBEntry.new(
				self.__db,
				self.__entry_type,
				"%s/item/%d/file" % (self.__base_url, item['id'])
			)
			self.__db.entry_set(entry, RB.RhythmDBPropType.TITLE, item['title'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.GENRE, item['genre'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.ARTIST, item['artist'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.ALBUM, item['album'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.TRACK_NUMBER, item['track'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.DISC_NUMBER, item['disc'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.DURATION, item['length'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.FILE_SIZE, item['size'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.BITRATE, int(item['bitrate'])/1000)
			self.__db.entry_set(entry, RB.RhythmDBPropType.COMMENT, item['comments'])
			self.__db.entry_set(entry, RB.RhythmDBPropType.ALBUM_ARTIST, item['albumartist'])
		self.__db.commit()
		
GObject.type_register(BeetsSource)
