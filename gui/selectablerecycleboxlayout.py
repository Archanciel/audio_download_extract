from kivy.properties import BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


class SelectableRecycleBoxLayout(FocusBehavior,
								 LayoutSelectionBehavior,
								 RecycleBoxLayout):
	''' Adds selection and focus behaviour to the view. '''
	
	MOVE_DIRECTION_UP = 'moveItemUp'
	MOVE_DIRECTION_DOWN = 'moveItemDown'
	
	# required to authorise unselecting a selected item
	touch_deselect_last = BooleanProperty(True)
	
	def get_nodes(self):
		nodes = self.get_selectable_nodes()
		
		if self.nodes_order_reversed:
			nodes = nodes[::-1]
		
		if not nodes:
			return None, None
		
		selected = self.selected_nodes
		
		if not selected:  # nothing selected
			return None, None
		
		if len(nodes) == 1:  # the only selectable node is selected already
			return None, None
		
		currentSelIdx = nodes.index(selected[-1])
		self.clear_selection()
		
		return currentSelIdx, nodes
