package byog.Core;

import byog.Core.Nodes.Player;
import byog.Core.TheWorld.NewWorld;
import byog.TileEngine.TERenderer;
import byog.TileEngine.TETile;

import java.awt.Color;
import java.awt.Font;
import java.io.File;
import java.io.IOException;

import edu.princeton.cs.introcs.StdDraw;

import javax.management.StringValueExp;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Scanner;


//rev. Implements serializable to save object.
public class Game {
    /* Feel free to change the width and height. */
    public static final int WIDTH = 75;
    public static final int HEIGHT = 35;
    private String seed = "";
    private int finds = 0;
    private char option;
    private static Player player;
    private String movement = "";
    private String allkeyinputs;
    private String validkeys = "aAsSdDwW";
    private static NewWorld world;
    private static TERenderer ter = new TERenderer(); //Sets up renderer
    private static TETile[][] finalWorldFrame;
    private static TETile[][] worldarray = new TETile[WIDTH][HEIGHT]; //Still need a TETile array.
    private int[] mouselocation = new int[2];
    private String description = "";
    private static int walks = 10;
    /**
     * Method used for playing a fresh game. The game should start from the main menu.
     */
    public void playWithKeyboard() {
        initializeCanvas();
        option = type();
        switch (option) {
            case 'n':
                seed = inputseed();
                walks = Integer.parseInt(walkks());
                newgame(seed);
                ter.renderFrame(world.getwworld());
                break;
            case 'N':
                seed = inputseed();
                walks = Integer.parseInt(walkks());
                newgame(seed);
                ter.renderFrame(world.getwworld());
                break;
            case 'l':
                loadgame();
                ter.renderFrame(finalWorldFrame);
                break;
            case 'L':
                loadgame();
                ter.renderFrame(finalWorldFrame);
                break;
            case 'q':
                break;
            case 'Q':
                break;
            default:
                break;
        }
        play();
    }

    public void play() {
        option = 'a';
        allkeyinputs = "";
        leftwalks();
        leftfruit();
        walleat();
        StdDraw.show();
        while (true) {
            if (StdDraw.hasNextKeyTyped()) {
                option = StdDraw.nextKeyTyped();
                allkeyinputs += option;
                finalWorldFrame = world.getWorld();
                if (validkeys.contains(String.valueOf(option))) {
                    world.move(option);
                    movement += option;
                    player.minuswalks();
                    finalWorldFrame = world.getWorld();
                    StdDraw.clear(Color.black);
                    leftwalks();
                    leftfruit();
                    walleat();
                    ter.renderFrame(finalWorldFrame);
                    StdDraw.show();
                }
                break;
            }
        }

        while (true) {
            try {
                mouselocation[0] = (int) Math.round(StdDraw.mouseX());
                mouselocation[1] = (int) Math.round(StdDraw.mouseY());
                if (mouselocation[0] < 0 || mouselocation[0] > WIDTH || mouselocation[1] > HEIGHT
                        || mouselocation[1] < 0) {
                    throw new ArrayIndexOutOfBoundsException("");
                }
                if (!description.equals(finalWorldFrame[mouselocation[0]][mouselocation[1]])) {
                    StdDraw.clear(Color.black);
                    leftwalks();
                    leftfruit();
                    walleat();
                    hud(mouselocation);

                }
            } catch (ArrayIndexOutOfBoundsException e) {
                System.out.print("");
            }
            if (StdDraw.hasNextKeyTyped()) {
                option = StdDraw.nextKeyTyped();
                allkeyinputs += option;
                if (validkeys.contains(String.valueOf(option))) {
                    world.move(option);
                    finalWorldFrame = world.getWorld();
                    movement += option;
                    player.minuswalks();
                    StdDraw.clear(Color.BLACK);
                    ter.renderFrame(finalWorldFrame);
                    leftwalks();
                    leftfruit();
                    walleat();
                    StdDraw.show();
                }
                if (allkeyinputs.contains(":q") || allkeyinputs.contains(":Q")) {
                    save();
                    break;
                }
            }
            if (player.getwalks() <= 0) {
                lose();
                break;
            }
            if (world.getFruit() == 0) {
                win();
                break;
            }

        }
    }

    public void initializeCanvas() {
        StdDraw.setCanvasSize(40 * 30, 40 * 30);
        StdDraw.setXscale(0, 40);
        StdDraw.setYscale(0, 40);
        StdDraw.setPenColor(100, 2, 3);
        Font font = new Font("Monaco", Font.BOLD, 20);
        StdDraw.setFont(font);
        StdDraw.clear();
        StdDraw.text(21, 30, "Eating is my life");
        StdDraw.text(21, 14, "New Eating (N)");
        StdDraw.text(21, 13, "Load Eating (L)");
        StdDraw.text(21, 12, "Quit Eating (Q)");
        StdDraw.show();
    }
    public char type() {
// rev. maybe need to improve the condition of while statement.
        while (option != 'q' && option != 'Q' && option != 'n' && option != 'N'
                && option != 'l' && option != 'L') {
            if (StdDraw.hasNextKeyTyped()) {
                option = StdDraw.nextKeyTyped();
            }
        }
        return option;
    }
    public String inputseed() {
        drawFrame("Please input seed");
        String str = "";
        char inputchar = 'a';
        while (inputchar != 's' && inputchar != 'S') {
            if (StdDraw.hasNextKeyTyped()) {
                inputchar = StdDraw.nextKeyTyped();
                str += String.valueOf(inputchar);
                drawFrame(str);
            }
        }
        return str.substring(0, str.length() - 1);
    }

    public String walkks() {
        drawFrame("Please input walks");
        String str = "";
        char inputchar = 'a';
        while (inputchar != 's' && inputchar != 'S') {
            if (StdDraw.hasNextKeyTyped()) {
                inputchar = StdDraw.nextKeyTyped();
                str += String.valueOf(inputchar);
                drawFrame(str);
            }
        }
        return str.substring(0, str.length() - 1);
    }


    public void drawFrame(String s) {
        StdDraw.clear();
        Font font = new Font("Arial", Font.BOLD, 32);
        StdDraw.setFont(font);
        StdDraw.text(20, 20, s);
        StdDraw.setPenColor(1, 200, 30);
        StdDraw.show();
    }
        /**
     * Method used for autograding and testing the game code. The input string will be a series
     * of characters (for example, "n123sswwdasdassadwas", "n123sss:q", "lwww". The game should
     * behave exactly as if the user typed these characters into the game after playing
     * playWithKeyboard. If the string ends in ":q", the same world should be returned as if the
     * string did not end with q. For example "n123sss" and "n123sss:q" should return the same
     * world. However, the behavior is slightly different. After playing with "n123sss:q", the game
     * should save, and thus if we then called playWithInputString with the string "l", we'd expect
     * to get the exact same world back again, since this corresponds to loading the saved game.
     * @param input the input string to feed to your program
     * @return the 2D TETile[][] representing the state of the world
     */
    public TETile[][] playWithInputString(String input) {
        // and return a 2D tile representation of the world that would have been
        // drawn if the same inputs had been given to playWithKeyboard().
        char options = input.charAt(0);
        switch (options) {
            case 'n':
                while (input.charAt(finds) != 's' && input.charAt(finds) != 'S') {
                    finds++;
                }
                seed = input.substring(1, finds);
                world = newgame(seed);
                finds += 1;
                for (; finds < input.length(); finds++) {
                    options = input.charAt(finds);
                    if (validkeys.contains(String.valueOf(options))) {
                        world.move(options);
                        movement += options;
                        finalWorldFrame = world.getWorld();
                    }
                }
                ter.renderFrame(world.getwworld());

                break;
            case 'N':
                while (input.charAt(finds) != 's' && input.charAt(finds) != 'S') {
                    finds++;
                }
                seed = input.substring(1, finds);
                world = newgame(seed);
                finds += 1;
                for (; finds < input.length(); finds++) {
                    options = input.charAt(finds);
                    if (validkeys.contains(String.valueOf(options))) {
                        world.move(options);
                        movement += options;
                        finalWorldFrame = world.getWorld();
                    }
                }
                ter.renderFrame(world.getwworld());
                break;
            case 'l':
                finalWorldFrame = loadgame();
                finds += 1;
                for (; finds < input.length(); finds++) {
                    options = input.charAt(finds);
                    if (validkeys.contains(String.valueOf(options))) {
                        world.move(options);
                        movement += options;
                        player.minuswalks();
                        finalWorldFrame = world.getWorld();
                    }
                }
                ter.renderFrame(finalWorldFrame);
                break;
            case 'L':
                finalWorldFrame = loadgame();
                finds += 1;
                for (; finds < input.length(); finds++) {
                    options = input.charAt(finds);
                    if (validkeys.contains(String.valueOf(options))) {
                        world.move(options);
                        movement += options;
                        player.minuswalks();
                        finalWorldFrame = world.getWorld();
                    }
                }
                ter.renderFrame(finalWorldFrame);
                break;
            default :
                break;
        }
        play();
        if (input.contains(":q") || input.contains(":Q")) {
            save();
        }
        return world.getwworld();
    }

    /*
        Made these methods directly in the Game class since I was prototyping for the most part.
        However, we should really put these into a new class, perhaps one called RoomGenerator
        or something of that nature. Also, if we want to add different kinds of rooms in the future
        then we might want to consider creating a super class for room shapes.

     */
//  @Source
//    I looked at here to implement serializable
// http://www.javapractices.com/topic/TopicAction.do?Id=57
//    https://stackoverflow.com/questions/731365/reading-and-displaying-data-from-a-txt-file
//    for scanner
    public TETile[][] loadgame() {
        try {
            ter.initialize(WIDTH, HEIGHT, 0, 2); //Initializes the screen
            Scanner fileIn1 = new Scanner(new File("./moves.txt"));
            Scanner fileIn2 = new Scanner(new File("./seed.txt"));
            Scanner fileIn3 = new Scanner(new File("./walks.txt"));
            walks = Integer.parseInt(fileIn3.nextLine());
            movement = fileIn1.nextLine();
            seed = fileIn2.nextLine();
            world = new NewWorld(WIDTH, HEIGHT, worldarray, Long.parseLong(seed), walks);
            world.generateRooms();
            world.canvas(); //Creates background.
            world.buildRooms(); //Renders the room.
            world.drawRooms();
            world.getNeighbors();
            world.drawHalls();
            world.renderNodes();
            finalWorldFrame = world.getWorld();
            world.renderNodes();
            for (int i = 0; i < movement.length(); i++) {
                world.move(movement.charAt(i));
                finalWorldFrame = world.getWorld();
            }
//            ter.renderFrame(finalWorldFrame); //Renders the map.
//            ter.renderFrame(world.getwworld()); //Renders the map.
        } catch (IOException e) {
            System.out.print("Cannot input a object");
        }
        player = world.getplayer();
        return finalWorldFrame;
    }

// @Source
//    https://stackoverflow.com/questions/2885173/how-do-i-create-a-file-and-write-to-it-in-java
//    looked at it for Files.write
    public void save() {
        try {
            Files.write(Paths.get("./moves.txt"), movement.getBytes());
            Files.write(Paths.get("./seed.txt"), seed.getBytes());
            Files.write(Paths.get("./walks.txt"), Integer.toString(player.getwalks()).getBytes());
        } catch (IOException e) {
            System.out.print("file out of bound");
        }
    }

    public static NewWorld newgame(String seed) {
        ter.initialize(WIDTH, HEIGHT, 0, 2); //Initializes the screen
        world = new NewWorld(WIDTH, HEIGHT, worldarray, Long.parseLong(seed), walks);
//        creates a World class.
        world.generateRooms();
//        Generate rooms of size s; tweaking needed to affect number of rooms.
        world.canvas(); //Creates background.
        world.buildRooms(); //Renders the room.
        world.drawRooms();
        world.getNeighbors();
        world.drawHalls();
        world.renderNodes();
        finalWorldFrame = world.getWorld();
        world.renderNodes();
//        ter.renderFrame(finalWorldFrame); //Renders the map.

//        ter.renderFrame(world.getwworld()); //Renders the map.
        player = world.getplayer();

        return world;
    }
    public void leftwalks() {
        Font font = new Font("Arial", Font.BOLD, 15);
        StdDraw.setFont(font);
        StdDraw.setPenColor(Color.white);
        String text = "Walks Left : " + Integer.toString(player.getwalks());
        StdDraw.text(30, 1, text);

    }

    public void leftfruit() {
        Font font = new Font("Arial", Font.BOLD, 15);
        StdDraw.setFont(font);
        StdDraw.setPenColor(Color.white);
        String text = "Fruits Left : " + Integer.toString(world.getFruit());
        StdDraw.text(40, 1, text);

    }

    public void walleat() {
        Font font = new Font("Arial", Font.BOLD, 15);
        StdDraw.setFont(font);
        StdDraw.setPenColor(Color.white);
        String text = "Wall-Eater Charges: " + Integer.toString(player.getWalleater());
        StdDraw.text(WIDTH - 20, 1, text);

    }

    public void hud(int[] mlocation) {
        try {
            if (mouselocation[0] < 0 || mouselocation[0] > WIDTH || mouselocation[1] > HEIGHT
                || mouselocation[1] < 0) {
                throw new ArrayIndexOutOfBoundsException("");
            }
            Font font = new Font("Arial", Font.BOLD, 15);
            StdDraw.setFont(font);
            StdDraw.setPenColor(Color.white);
            String text = world.getWorld()[mlocation[0] - 1][mlocation[1] - 3].description();
            text = text.toUpperCase();
            StdDraw.text(10, 1, text);
            ter.renderFrame(finalWorldFrame);
            StdDraw.show();
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.print("");
        }
    }

    public static void win() {
        StdDraw.clear(Color.BLACK);
        Font font = new Font("Monaco", Font.BOLD, 30);
        StdDraw.setFont(font);
        StdDraw.setPenColor(Color.white);
        StdDraw.text(WIDTH / 2, HEIGHT / 2, "Satisfied with the fruits. Let's go another eating!");
        StdDraw.show();
    }

    public static void lose() {
        StdDraw.clear(Color.BLACK);
        Font font = new Font("Monaco", Font.BOLD, 30);
        StdDraw.setFont(font);
        StdDraw.setPenColor(Color.white);
        StdDraw.text(WIDTH / 2, HEIGHT / 2, "Lack of sugar... I can't walk anymore...");
        StdDraw.show();

    }
    public static void main(String[] args) {
    }
}
