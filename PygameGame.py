import pygame
import random

'''
pygamegame.py framework borrowed from Lukas Peraza
 from 15-112 F15 Pygame Optional Lecture, 11/11/15
'''
#Global variables 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

INGREDIENTS = {"coffee":"Small_Images/Ingredients/CoffeeBean.png",
               "ice":"Small_Images/Ingredients/IceCubes.png",
               "milk":"Small_Images/Ingredients/Milk.png",
               "water":"Small_Images/Ingredients/Water.png",
               "chocolate":"Small_Images/Ingredients/Chocolate.png",
               "vanilla":"Small_Images/Ingredients/Vanilla.png",
               "whipped cream":"Small_Images/Ingredients/WhippedCream.png"}

RECIPES = {"Brewed Coffee":((1, "coffee"), (3, "water")), 
                "Iced Coffee":((1, "coffee"), (2, "water"), (1, "ice")),
                "Iced Coffee w/ Milk":((1, "coffee"), (1, "milk"), (1, "ice")),
                "Caffe Misto":((2, "coffee"), (2, "milk")),
                "Caffe Americano":((2, "water"), (2, "coffee")),
                "Caffe Mocha":((1, "milk"), (1, "coffee"), (1, "chocolate"), (1, "whipped cream")),
                "Caffe Latte": ((2, "milk"), (2, "coffee")),
                "Vanilla Latte": ((1, "vanilla"), (1, "milk"), (2, "coffee")),
                "Iced Vanilla Latte": ((1, "vanilla"), (1, "milk"), (1, "coffee"), (1, "ice"))}

SECRET_RECIPES = {"Vanilla Frappuccino": ((2, "ice"), (1, "vanilla"), (1, "milk")),
                  "Coffee Frappuccino": ((2, "ice"), (1, "coffee"), (1, "milk"))}

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.image = pygame.image.load('Small_Images/cup.png').convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):
        pos = pygame.mouse.get_pos()
        # sets the player's x position to the mouse x position
        if (pos[0] < 790):
            self.rect.x = pos[0]
        elif (pos[0] > 790):
            self.rect.x = 790
        self.rect.y = 625

class Recipes(object):

    def __init__(self):
        #chooses random recipe
        self.recipeName = random.choice(list(RECIPES.keys()))

        self.recipe = RECIPES[self.recipeName]
        
        #makes the 2d-tuple a 2d-list
        self.ingredientsNeeded = []
        for element in self.recipe:
            self.ingredientsNeeded += [list(element)]

        self.ingredientsCaught = []

    def add(self, ingredient):
        #ingredient is in the form of 2d list
        if ingredient in self.ingredientsCaught:
            index = self.ingredientsCaught.index(ingredient)
            self.ingredientsCaught[index][0] += 1
        else: self.ingredientsCaught.append(ingredient)

    def checkIfRecipeDone(self):
        if self.ingredientsCaught == self.ingredientsNeeded:
            return True
        elif self.ingredientsCaught != self.ingredientsNeeded:
            return False

    def checkIfValidIngredient(self): 
        newList = []

        for elements in self.ingredientsNeeded:
            newList.append(elements[1])

        for caughtElements in self.ingredientsCaught:
            if caughtElements[1] not in newList:
                return False

class Customers(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Small_Images/Customer.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.recipe = Recipes() #assigns a recipe to each customer
        self.time = 0
        self.count = 0 

    def update(self):
        self.count += 1 
        if (self.count % 30 == 0):
            self.time += 1 

class Ingredients(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ingredient = random.choice(list(INGREDIENTS.keys()))
        self.image = pygame.image.load(INGREDIENTS[self.ingredient]).convert_alpha()
        self.rect = self.image.get_rect()
 
    def update(self):
        self.rect.y += 1

class PygameGame(object):

    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1400, height=700, fps=60, title="Barista Trainer"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.mode = "intro"
        self.learnType = "classic"
        self.gameWindowX = 915
        self.gameWindowY = 187
        self.recipe = random.choice(list(RECIPES.keys()))
        self.learnRecipe = None
        self.shiftTime = 120
        self.numCustomers = 1
        self.currentCustomer = None
        self.totalMoney = 0
        self.level = "easy"
        self.gameOver = False
        pygame.init()

    def runWinScreen(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                    self.gameOver = False
                    self.mode = "intro"
                    self.runIntro()
                    
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            bg = pygame.image.load('Screens/WinScreen.png').convert_alpha()
            screen.blit(bg, (0, 0))

            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

    def runGameOverScreen(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                    self.gameOver = False
                    self.mode = "intro"
                    self.runIntro()
                    
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            bg = pygame.image.load('Screens/GameOverScreen.png').convert_alpha()
            screen.blit(bg, (0, 0))

            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()

    def runGameplay(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        # stores all the keys currently being held down
        self._keys = dict()
        ingredientsList = pygame.sprite.Group()
        # call game-specific initialization
        self.init()
        playing = True

        count = 0 
        shiftTime = 0

        all_sprites_list = pygame.sprite.Group()
        player = Player()
        all_sprites_list.add(player)

        #initializes first customer
        listOfCustomers = []
        customer = Customers() 
        all_sprites_list.add(customer)
        listOfCustomers.append(customer)
        self.currentCustomer = customer

        while playing:
            for customer in listOfCustomers: 
                #determines placement of the customer
                j = listOfCustomers.index(customer) 
                customer.rect.x = 140*j
                customer.rect.y = 30

            for i in range(6):
                if (count%130 == 0):
                    ingredient = Ingredients()
                    ingredient.rect.x = random.randrange(self.gameWindowX-30)
                    ingredient.rect.y = random.randrange(187, 345)
                    all_sprites_list.add(ingredient)
                    ingredientsList.add(ingredient)

            if (count%1000==0):
                newCustomer = Customers()
                listOfCustomers.append(newCustomer)
                all_sprites_list.add(newCustomer)

            if (count % 30 == 0):
                shiftTime += 1 

            for customers in listOfCustomers:
                if customers.time > 100:
                    listOfCustomers.remove(customers)

            time = clock.tick(self.fps)
            self.timerFired(time)

            for event in pygame.event.get():
                print(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                    #if quit button pressed, return to intro screen
                    if (event.pos[1] < 142 and event.pos[1] > 11 and event.pos[0] > 1343 and event.pos[0] < 1388):
                        self.mode = "intro"
                        self.runIntro()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            
            #Ingredient-cup collision
            for ingredient in ingredientsList: 

                ingredientsHitList = pygame.sprite.spritecollide(player, ingredientsList, True)

                for hitIngredient in ingredientsHitList: 
                    ingredientsList.remove(hitIngredient)
                    self.currentCustomer.recipe.add([1, hitIngredient.ingredient])

                if self.currentCustomer.recipe.checkIfValidIngredient() == False:
                    player.lives -= 1
                    listOfCustomers.pop(0)
                    try: 
                        self.currentCustomer = listOfCustomers[0]
                    except: 
                        newCustomer = Customers()
                        listOfCustomers.append(newCustomer)
                        all_sprites_list.add(newCustomer)
                        self.currentCustomer = listOfCustomers[0]

                if self.currentCustomer.recipe.checkIfRecipeDone() == True:
                    listOfCustomers.pop(0)
                    self.currentCustomer = listOfCustomers[0]

                if ingredient.rect.y > (self.height-100):
                    ingredientsList.remove(ingredient)

            print(self.currentCustomer.recipe.ingredientsCaught)
            if player.lives == 0: 
                self.mode = "game over"
                self.runGameOverScreen()

            print(self.currentCustomer.recipe.ingredientsCaught)
            print(self.currentCustomer.recipe.ingredientsNeeded)

            count += 1

            bg = pygame.image.load('Screens/GameplayScreen.png').convert_alpha()
            screen.blit(bg, (0, 0))

            #draws hearts to represent number of lives left
            livesfont=pygame.font.Font(None,16)
            livesText =livesfont.render("LIVES: ", 1, WHITE)
            screen.blit(livesText, (1254,625))
            heart = pygame.image.load('Small_Images/heart.png').convert_alpha()
            for i in range(player.lives):
                screen.blit(heart, (1254+35*i, 640)) 

            #draws "Recipe Card"
            recipeCardTitleFont=pygame.font.Font(None,40)
            titleText = recipeCardTitleFont.render("Recipe Card", 1, WHITE)
            screen.blit(titleText, (1075,200))

            #draws name of recipe
            recipeTitleFont=pygame.font.Font(None,30)
            titleText = recipeTitleFont.render(self.currentCustomer.recipe.recipeName + ":", 1, WHITE)
            screen.blit(titleText, (970,260))

            #draws recipe text
            recipeFont = pygame.font.Font(None,30)
            ingCount = 0 
            for element in self.currentCustomer.recipe.recipe:
                recipeText = "  " + str(element[0]) + " " + element[1]
                text = recipeFont.render(recipeText, 1, WHITE)
                screen.blit(text, (970,300+35*ingCount))
                ingCount += 1 

            #draws info on top right corner of screen
            timeFont=pygame.font.Font(None,30)
            titleText = timeFont.render("Time Left: " + str(30-self.currentCustomer.time), 1, WHITE)
            screen.blit(titleText, (1154,12))

            titleText = timeFont.render("Total Time Left: " + str(120-shiftTime), 1, WHITE)
            screen.blit(titleText, (1154,30))

            if (self.currentCustomer.time > 30): 
                try: 
                    self.currentCustomer = listOfCustomers[1]
                    listOfCustomers.pop(0)

                except: 
                    listOfCustomers.pop(0)

            if (shiftTime >= self.shiftTime):
                self.mode = "win"
                self.runWinScreen()

            if (listOfCustomers == []): 
                self.gameOver = True

            if (self.gameOver == True):
                self.mode = "game over"
                self.runGameOverScreen()

            self.redrawAll(screen)
            all_sprites_list.update()
            ingredientsList.update()
            all_sprites_list.draw(screen)
            ingredientsList.draw(screen)
            pygame.display.flip()

        pygame.quit()

    def runLearn(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
        self.init()
        playing = True

        while (playing == True):
            time = clock.tick(self.fps)
            self.timerFired(time)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                    #if quit button pressed, return to intro screen
                    if (event.pos[1] < 88 and event.pos[1] > 39 and event.pos[0] > 1231 and event.pos[0] < 1368):
                        self.mode = "intro"
                        self.runIntro()
                    elif (event.pos[1] < 215 and event.pos[1] > 156 and event.pos[0] > 73 and event.pos[0] < 289):
                        self.learnType = "classic"
                        self.learnRecipe = None
                    elif (event.pos[1] < 300 and event.pos[1] > 239 and event.pos[0] > 73 and event.pos[0] < 289):
                        self.learnType = "secret"
                        self.learnRecipe = None
                    #if within the clicking box
                    if self.learnType == "classic":
                        if (event.pos[1] < 201 and event.pos[1] > 152 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Brewed Coffee"
                        elif (event.pos[1] < 250 and event.pos[1] > 201 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Iced Coffee"  
                        elif (event.pos[1] < 299 and event.pos[1] > 250 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Iced Coffee w/ Milk" 
                        elif (event.pos[1] < 348 and event.pos[1] > 299 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Caffe Misto"  
                        elif (event.pos[1] < 397 and event.pos[1] > 348 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Caffe Americano"  
                        elif (event.pos[1] < 446 and event.pos[1] > 397 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Caffe Mocha"  
                        elif (event.pos[1] < 495 and event.pos[1] > 446 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Caffe Latte"  
                        elif (event.pos[1] < 544 and event.pos[1] > 495 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Vanilla Latte" 
                        elif (event.pos[1] < 593 and event.pos[1] > 544 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Iced Vanilla Latte"  
                    elif self.learnType == "secret":
                        if (event.pos[1] < 201 and event.pos[1] > 152 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Vanilla Frappuccino"
                        elif (event.pos[1] < 250 and event.pos[1] > 201 and event.pos[0] > 365 and event.pos[0] < 586):
                            self.learnRecipe = "Coffee Frappuccino"  
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            if (self.learnType == "classic"):
                recipeScreen = pygame.image.load('Screens/LearnRecipeScreen-Classic.png').convert_alpha()
            elif (self.learnType == "secret"):
                recipeScreen = pygame.image.load('Screens/LearnRecipeScreen-Secret.png').convert_alpha()
            screen.blit(recipeScreen, (0, 0))


            text = ""
            #print recipe on the side
            if (self.learnRecipe == None): 
                font=pygame.font.Font(None,30)
                noneText =font.render("Please select a recipe from the menu to the left", 1, WHITE)
                screen.blit(noneText, (717, 196))
            elif (self.learnRecipe != None) and (self.learnType == "classic"):
                #text = ""
                for element in RECIPES[self.learnRecipe]:
                    if text == "":
                        text = text + str(element[0]) + " " + element[1]
                    else: 
                        text = text + ", " + str(element[0]) + " " + element[1]
            elif (self.learnRecipe != None) and (self.learnType == "secret"):
                #text = ""
                for element in SECRET_RECIPES[self.learnRecipe]:
                    if text == "":
                        text = text + str(element[0]) + " " + element[1]
                    else: 
                        text = text + ", " + str(element[0]) + " " + element[1]

            displayRecipeText = font.render(text, 1, WHITE)
            screen.blit(displayRecipeText, (717, 250))
            titleFont=pygame.font.Font(None,50)
            recipeTitle = titleFont.render(self.learnRecipe, 1, WHITE)
            screen.blit(recipeTitle, (717, 190))
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()

    def runIntro(self):
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while (playing == True and self.mode == "intro"):
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self.mousePressed(*(event.pos))
                    #instructions button
                    if (event.pos[1] < 588 and event.pos[1] > 531 and event.pos[0] > 73 and event.pos[0] < 289):
                        self.mode == "instructions"
                    #play button
                    elif (event.pos[1] < 590 and event.pos[1] > 532 and event.pos[0] > 1115 and event.pos[0] < 1334):
                        self.mode == "gameplay"
                        self.runGameplay()
                    elif (event.pos[1] < 590 and event.pos[1] > 532 and event.pos[0] > 770 and event.pos[0] < 989):
                        self.mode == "learn"
                        self.runLearn()
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        self.mouseReleased(*(event.pos))
                    elif (event.type == pygame.MOUSEMOTION and
                          event.buttons == (0, 0, 0)):
                        self.mouseMotion(*(event.pos))
                    elif (event.type == pygame.MOUSEMOTION and
                          event.buttons[0] == 1):
                        self.mouseDrag(*(event.pos))
                    elif event.type == pygame.KEYDOWN:
                        self._keys[event.key] = True
                        self.keyPressed(event.key, event.mod)
                    elif event.type == pygame.KEYUP:
                        self._keys[event.key] = False
                        self.keyReleased(event.key, event.mod)
                    elif event.type == pygame.QUIT:
                        playing = False
            start = pygame.image.load('Screens/StartScreen.png').convert_alpha()
            screen.blit(start, (0, 0))
            self.redrawAll(screen)
            pygame.display.flip()
        pygame.quit()


game = PygameGame()
game.runIntro()

