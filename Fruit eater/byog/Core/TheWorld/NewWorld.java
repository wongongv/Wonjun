package byog.Core.TheWorld;

import byog.Core.Game;
import byog.Core.RandomUtils;
import byog.Core.Room;
import byog.Core.Nodes.Portal;
import byog.Core.Nodes.Player;
import byog.TileEngine.TETile;
import byog.TileEngine.Tileset;
import java.util.Random;


public class NewWorld {

    //Dimensions
    int width;
    int height;
    int nor;

    private TETile[][] bb;
    private Room[] rooms;
    private static TETile[][] world;
    private Portal[] portals;
    private Random absurdity;
    private Visualizer vis;
    private Player player;
    private TETile[] walls;
    private TETile[] foods;
    private int fruits;

    public NewWorld(int w, int h, TETile[][] wd, long seed, int walks) {
        width = w;
        height = h;
        world = wd;
        absurdity = new Random(seed);
        player = new Player(0, 0, walks);
        rooms = new Room[RandomUtils.uniform(absurdity, 15, 20)];
        walls = new TETile[] {Tileset.WALL, Tileset.WALL2, Tileset.WALL3, Tileset.WALL4};
        foods = new TETile[] {Tileset.FOOD1, Tileset.FOOD2, Tileset.FOOD3};
        portals = new Portal[4];
        bb = new TETile[w][h];
        vis = new Visualizer(width, height, world, absurdity, bb);
        fruits = rooms.length - 5;
    }

    /** Here lies the stuff that sets up the room skeleton. **/

    private int[] setParams(int size) { //Does the actual work for defining random room parameters.
        int w = randint(4, size);
        int h = randint(4, size);
        int xcor = randint(1, width - w);
        int ycor = randint(1, height - h - 2);
        int xnode = xcor + randint(1, w - 1);
        int ynode = ycor + randint(1, h - 1);
        return new int[] {w, h, xcor, ycor, xnode, ynode};
        //returns the "specs" used by Room Constructor.
    }

    private Room createRoom(int size) {
        //Creates and filters out random Room instance;
        //Only returns Room instances that don't overlap.
        boolean canpass = false;
        int[] room = setParams(size);
        if (nor == 0) {
            return new Room(room);
        } else {
            while (!canpass) {
                canpass = !isoccupied(room[2], room[3], room[0], room[1]);
                if (!canpass) {
                    room = setParams(size);
                }
            }
        }
        return new Room(room);
    }

    public void generateRooms() { //Instantiates and adds rooms to the list of rooms.
        while (nor < rooms.length) {
            int size = RandomUtils.uniform(absurdity, 10, 20);
            Room newroom = createRoom(size);
            rooms[nor] = newroom;
            nor++;
        }
    }

    public void getNeighbors() {
        for (Room room1 : rooms) {
            for (Room room2 : rooms) {
                if (room1 != room2) {
                    int[] coord1 = room1.getHallnode();
                    int[] coord2 = room2.getHallnode();
                    int x = Math.abs(coord1[0] - coord2[0]);
                    int y = Math.abs(coord1[1] - coord2[0]);
                    if (x <= RandomUtils.uniform(absurdity,  width / 3, width)
                            && y <= RandomUtils.uniform(absurdity, height / 2, height)) {
                        room1.addneighbor(room2);
                    }
                }
            }
        }
    }

    /** Visual Methods facilitated by the Visualizer **/
    public void drawRooms() {
        vis.buildRooms(rooms);
    }

    public void drawHalls() {
        vis.drawhalls(rooms);
    }

    public void renderNodes() {
        vis.dotyourts(rooms);
        portalmake();
        int x = rooms[0].getHallnode()[0];
        int y = rooms[0].getHallnode()[1];
        player.setCoords(x, y);
    }

    public void canvas() {
        vis.canvas();
    }

    public void buildRooms() {
        vis.buildRooms(rooms);
    }


    /** PORTAL METHODS **/

    private void portalmake() {
        for (int i = 1; i < 5; i++) {
            int x = rooms[i].getHallnode()[0];
            int y = rooms[i].getHallnode()[1];
            portals[i - 1] = new Portal(x, y, null);
        }
        pairportal(portals[0], portals[1]);
        pairportal(portals[2], portals[3]);

    }

    private void pairportal(Portal x, Portal y) {
        x.setpart(y);
        y.setpart(x);
    }

    private Portal getPortal(int[] coords) {
        Portal porto = new Portal();
        for (Portal portal : portals) {
            if (portal.isme(coords)) {
                porto = portal;
            }
        }
        return porto;
    }

    private int[] clearzone(Portal portal) {
        int x = portal.getx();
        int y = portal.gety();
        int[] newcoords;
        while (true) {
            newcoords = new int[] {randint(x - 1, x + 1), randint(y - 1, y + 1)};
            if (!portal.isme(newcoords)) {
                if (!isWall(world[newcoords[0]][newcoords[1]])) {
                    break;
                }
            }
        }
        return newcoords;
    }

    /** Player Functions **/

    public void move(char option) {
        option = Character.toLowerCase(option);
        int x = player.getcoords()[0];
        int y = player.getcoords()[1];
        int copyx = x;
        int copyy = y;
        switch (option) {
            case 'a':
                x--;
                break;
            case 's':
                y--;
                break;
            case 'd':
                x++;
                break;
            case 'w':
                y++;
                break;
            default :
                break;
        }
        if (x < 0 || x >= width || y < 0 || y >= height) {
         player.pluswalks(1);
        } else if (isWall(world[x][y])) {
            if (player.caneat()) {
                world[copyx][copyy] = Tileset.FLOOR;
                player.move(option);
                player.eattick();
                updateplayer();
            } else {
                player.pluswalks(1);}

        } else if (world[x][y] == Tileset.PORTAL) {
            world[copyx][copyy] = Tileset.FLOOR;
            Portal port = getPortal(new int[] {x, y});
            int[] newloc = clearzone(port.pcoords());
            player.teleport(newloc);
            blackout(copyx, copyy);
            updateplayer();
        } else {
            if (isFood(world[x][y])) {
                switch (world[x][y].description()) {
                    case "Stone Melon (Eat through walls!)":
                        fruits--;
                        player.raisetick(4);
                        player.pluswalks(20);
                        break;
                    case "Light Berry (Increased Vision!)":
                        fruits--;
                        player.raisevis();
                        player.pluswalks(15);
                        break;
                    case "Honey Fruit (+30 movement!)":
                        fruits--;
                        player.pluswalks(30);
                        break;
                    default:
                        System.out.println(world[x][y].description());
                }
            }
            world[copyx][copyy] = Tileset.FLOOR;
            player.move(option);
            updateplayer();
        }
    }


    public void updateplayer() {
        vis.updateplayer(player.getcoords());
    }

    private boolean isFood(TETile tile) {
        boolean is = false;
        for (TETile food : foods) {
            if (tile == food) {
                is = true;
            }
        }
        return is;
    }

    private boolean isWall(TETile tile) {
        boolean is = false;
        for (TETile wall : walls) {
            if (tile == wall) {
                is = true;
            }
        }
        return is;
    }


    /** Misc. Helper Functions **/

    private boolean isoccupied(int left, int bottom, int w, int h) {
        //Slightly modified and significantly more verbose version of original isoccupied.
        //Technically the structure has not been changed at all, only the renaming of vars
        //and the addition of an if condition to handle nulls.

        /* NEEDS REVISION!!!!!! */

        for (int i = 0; i < rooms.length; i++) {
            Room j = rooms[i];
            if (j != null) {
                if (left <= j.getcorner(3).getx() && left >= j.getcorner(0).getx()
                        && bottom <= j.getcorner(3).gety()
                        && bottom >= j.getcorner(0).gety()) {
                    return true;
                } else if (left <= j.getcorner(0).getx() && bottom <= j.getcorner(3).gety()
                        && bottom >= j.getcorner(0).gety()
                        && left + w >= j.getcorner(0).getx()) {
                    return true;
                } else if (left <= j.getcorner(3).getx() && left >= j.getcorner(0).getx()
                        && bottom <= j.getcorner(0).gety()
                        && bottom + h >= j.getcorner(0).gety()) {
                    return true;
                } else if (left < j.getcorner(0).getx() && bottom < j.getcorner(0).gety()
                        && bottom + h >= j.getcorner(0).gety()
                        && left + w >= j.getcorner(0).getx()) {
                    return true;
                }
            }
        }
        return false;
    }

    public TETile[][] getWorld() {
        int x = player.getx();
        int y = player.gety();
        int q;
        int p;
        int vision = player.vision() + 1;
        for (int i = -vision; i < vision + 1; i++) {
            for (int o = -vision; o < 1 + vision; o++) {
                q = x + i;
                p = y + o;
                if (q >= width || q < 0 || p >= height || p < 0) {

                } else if (Math.abs(i) == vision || Math.abs(o) == vision) {
                    bb[q][p] = Tileset.NOTHING;
                } else {
                    bb[q][p] = world[q][p];
                }
            }
        }
        return bb;
    }

    public void blackout(int x, int y) {
        int q;
        int p;
        int vision = player.vision() + 1;
        for (int i = -vision; i < vision + 1; i++) {
            for (int o = -vision; o < 1 + vision; o++) {
                q = x + i;
                p = y + o;
                if (q >= width || q < 0 || p >= height || p < 0) {

                } else{
                    bb[q][p] = Tileset.NOTHING;
                }
            }
        }
    }

    private int randint(int start, int end) {
        //Makeshift implementation of randint with a range.
        int randnum = absurdity.nextInt((end - start)) + start;
        return randnum;
    }

    public TETile[][] getwworld() {
        return world;
    }

    public Player getplayer() {
        return player;
    }

    public int getFruit() {
        return fruits;
    }
}
