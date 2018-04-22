from PyQt4.QtCore import Qt, QPointF, QRectF
from PyQt4.QtGui import QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, QVBoxLayout, QSpacerItem, QSizePolicy, QCursor, QSizeGrip

class DraggableBox( QGraphicsItem ):
    """
    A simple QGraphicsItem that can be dragged around the scene.
    Of course, this behavior is easier to achieve if you simply use the default 
    event handler implementations in place and call 
    QGraphicsItem.setFlags( QGraphicsItem.ItemIsMovable )
    
    ...but this example shows how to do it by hand, in case you want special behavior 
    (e.g. only allowing left-right movement instead of arbitrary movement). 
    """
    
    def __init__(self, parent, *args, **kwargs):
        super( DraggableBox, self ).__init__( parent, *args, **kwargs )
        self.setAcceptHoverEvents(True)
     
    def boundingRect(self):
        return QRectF( 0, 0, 30, 10)
    
    def paint(self, painter, option, widget):
        painter.drawText( QPointF(0,10), "Hiya" )
        painter.drawRect( self.boundingRect() )

    def hoverEnterEvent(self, event):
        cursor = QCursor( Qt.OpenHandCursor )
        QApplication.instance().setOverrideCursor( cursor )
    
    def hoverLeaveEvent(self, event):
        QApplication.instance().restoreOverrideCursor()
    
    def mouseMoveEvent(self, event):
        new_pos = event.scenePos()

        # Keep the old Y position, so only the X-pos changes.
        old_pos = self.scenePos()
        new_pos.setY( old_pos.y() )
        
        self.setPos( new_pos )

    # We must override these or else the default implementation prevents 
    #  the mouseMoveEvent() override from working.
    def mousePressEvent(self, event): pass        
    def mouseReleaseEvent(self, event): pass

if __name__ == "__main__":
    app = QApplication([])
    
    rect = QRectF(0, 0, 150, 150 )
    
    scene = QGraphicsScene()
    scene.addRect( rect )

    view = QGraphicsView( scene )
    view.setSceneRect( rect )


    w = QWidget()
    w.setLayout( QVBoxLayout() )
    w.layout().addWidget(view)
    w.layout().addWidget(QSizeGrip(view))
    # w.layout().addSpacerItem( QSpacerItem(0, 0, QSizePolicy.Expanding) )
    w.show()
    w.raise_()
    
    box = DraggableBox( None, scene=scene )
    box.setPos( 10,20 )
    #box.setRotation(45)
    
app.exec_()