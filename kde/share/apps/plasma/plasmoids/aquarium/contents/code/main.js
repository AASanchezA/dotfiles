/*
 * Aquarium, a small fishbowl for your desktop.
 *
 * Copyright 2010 by Ontje Lünsdorf <The_COM@gmx.de>
 *
 * This program is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation; either version 3 of the License, or (at your option) any later
 * version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; if not, see <http://www.gnu.org/licenses/>
 *
 */

/*
 * Description
 * -----------
 *
 * This applet tries to simulate the behavior of fish swarms. It's based on the
 * boid algorithm from Craig Reynolds, see <http://www.red3d.com/cwr/boids/>.
 *
 * The algorithm has been enhanced with feeding and mating behaviors. A very
 * simple form of evolution is also modelled. So feed your fishes properly and
 * see the sea holds in store for you! Who knows, maybe you will even spot
 * the famous jaguar shark!
 *
 * Thanks to my brother Gerrit Lünsdorf and his girlfriend Johanna Carola Fokken
 * for pinkfish and seahorse. Also thanks to Stefan Scherfke for the porcupine
 * fish.
 */

// --- Constants.

var BubbleTime = 2000;
var MinAutofeedTime = 2000, MaxAutofeedTime = 5000;
var AutoBuyLimit = 5, AutobuyTime = 2000;
var Features = [
    [0.1, "castle"], [0.5, "seaweed1"], [0.5, "seaweed2"], [0.5, "seaweed3"],
    [0.1, "skull"], [0.1, "treasure"], [1, "sand1"], [1, "sand2"], [1, "sand3"]
];

// Some pens.
red_pen = new QPen();
red_pen.color = new QColor(255, 0, 0);

green_pen = new QPen();
green_pen.color = new QColor(0, 255, 0);

blue_pen = new QPen();
blue_pen.color = new QColor(0, 0, 255);

white_pen = new QPen();
white_pen.color = new QColor(255, 255, 255);

// Food constants.
FoodType = 2;
food_pixmap = new Svg("food").pixmap();

// Bubble constants.
BubbleType = 3;
bubble_pixmap = new Svg("bubble").pixmap();

// Boid constants.
BoidType = 1;
Male = 0; Female = 1;
MinBoidSize = 0.5;
AgeStages = 10;
ShowInfo = false;

// FishType description:
// [
//      pixmap, min_age, max_age, min_energy, max_energy,
//      min_avg_speed, max_avg_speed, min_breedtime, max_breedtime
// ]

FishTypes = [
    [Svg("fish1").pixmap(), 3 * 60, 10 * 60, 50, 100, 10, 20, 10, 30],
    [Svg("pinkfish").pixmap(), 3 * 60, 10 * 60, 100, 100, 10, 30, 10, 30],
    [Svg("fish2").pixmap(), 3 * 60, 10 * 60, 100, 100, 10, 30, 10, 30],
    [Svg("fish4").pixmap(), 3 * 60, 10 * 60, 100, 100, 10, 30, 10, 30],
    [Svg("fish3").pixmap(), 3 * 60, 10 * 60, 100, 100, 20, 30, 10, 30],
    [Svg("seahorse").pixmap(), 3 * 60, 6 * 60, 100, 100, 10, 20, 10, 30],
    [Svg("jaguarshark").pixmap(), 3 * 60, 6 * 60, 100, 100, 20, 30, 10, 30]
];

// --- Convenience methods.
create_fish = function(x, y, value) {
    // Create a fish and select its characterists from FishTypes based on its
    // value.
    var new_value = Math.min(uniform(value / 2, value), FishTypes.length);
    var type = FishTypes[Math.floor(new_value)];

    var pixmap = type[0];
    var max_age = uniform(type[1], type[2]);
    var energy = uniform(type[3], type[4]);
    var avg_speed = uniform(type[5], type[6]);
    var breed_time = uniform(type[7], type[8]);

    return new Boid(
            x, y, pixmap, new_value, max_age, energy, avg_speed, breed_time);
}

create_default_fish = function() {
    var x_max = plasmoid.rect.width / 2;
    var y_max = plasmoid.rect.height / 2;
    return create_fish(
            uniform(-x_max, x_max), uniform(-y_max, y_max), Math.random());
}

distance = function(x, y) {
    // Returns the distance of a vector to the origin.
    return Math.sqrt(x * x + y * y);
}

angle_between = function(a_x, a_y, b_x, b_y) {
    // Returns the angle between two vectors.
    var d = distance(a_x, a_y) * distance(b_x, b_y);
    if(d < 0.01) return 0;
    return Math.acos((a_x * b_x + a_y * b_y) / d);
}

uniform = function(a, b) {
    // Convenience method to return a float between a and b.
    return a + Math.random() * (b - a);
}

delta = function(p1, p2) {
    // Difference between two vectors.
    return new Point(p2.x - p1.x, p2.y - p1.y);
}

scale = function(p1, s) {
    // Returns a scaled instance of a vector.
    return new Point(p1.x * s, p1.y * s);
}

// --- Classes.
Point = function(x, y) {
    // A generic vector with some utility functions.
    this.x = x;
    this.y = y;

    this.len = function() {
        return distance(this.x, this.y);
    }

    this.add = function(other) {
        this.x += other.x; this.y += other.y;
    }

    this.scale = function(a) {
        this.x *= a; this.y *= a;
        return this;
    }

    this.reset = function() {
        this.x = 0; this.y = 0;
    }

    this.normalize = function() {
        var l = this.len();

        if(l > 0.01) {
            this.x /= l; this.y /= l;
        } else {
            this.x = 0; this.y = 0;
        }
    }

    this.str = function() {
        return this.x.toFixed(2) + ", " + this.y.toFixed(2);
    }
}

Entity = function(x, y, size, pixmap) {
    // The base class for visual objects like food, fishes and bubbles.
    this.type = undefined;

    this.pos = new Point(x, y);
    this.size = size;
    this.direction = new Point(0, 0);
    this.orig_pixmap = pixmap;

    this.pixmap = undefined;
    this.pix_ofs = undefined;

    this.resize = function() {
        this.pixmap = this.orig_pixmap.scaled(
            this.orig_pixmap.rect.width * this.size,
            this.orig_pixmap.rect.height * this.size);

        this.pix_ofs = new Point(
            -this.pixmap.rect.width / 2, -this.pixmap.rect.height / 2);
    }

    // Initiate pixmap.
    this.resize();

    this.paint = function(painter) {
        painter.save();
        if(this.direction.x > 0)
            painter.scale(-1, 1);
        painter.drawPixmap(this.pix_ofs.x, this.pix_ofs.y, this.pixmap);
        painter.restore();
    }

    this.move = function() {
        this.pos.add(this.direction);
    }

    this.alive = function() {
        return true;
    }
}

Food = function(x, y) {
    // Food to be eaten by fishes.
    Entity.call(this, x, y, uniform(0.5, 1), food_pixmap);
    this.type = FoodType;

    this.direction = new Point(0, 1);
    this.speed = uniform(2.5, 7.5);

    this.alive = function() {
        return (
            this.size > 0 &&
            this.pos.y < (plasmoid.rect.height * 0.5) * 0.9
        );
    }

    this.eat = function() {
        var amount = Math.min(this.size, 0.1);
        this.size -= amount;
        this.resize();
        return amount * 50;
    }
}

Bubble = function(x, y) {
    // Just a bubble.
    Entity.call(this, x, y, uniform(0.5, 1), bubble_pixmap);

    this.type = BubbleType;

    this.direction = new Point(0, -1);
    this.speed = uniform(10, 30);

    this.alive = function() {
        return this.pos.y > -(plasmoid.rect.height * 0.5) * 0.9;
    }
}

Boid = function(x, y, pixmap, value, max_age, energy, average_speed,
        breed_time) {
    // A boid that models the fishes behavior.
    Entity.call(this, x, y, MinBoidSize, pixmap);

    this.value = value;
    this.average_speed = average_speed;
    this.energy = energy;
    this.max_age = max_age;
    this.breed_time = breed_time;
    this.type = BoidType;

    this.acceleration = 0;
    this.speed = this.average_speed;
    this.age = 0;
    this.next_breed = this.breed_time;
    this.age_stage = 0;

    var pixmap_size =
        (this.orig_pixmap.rect.width + this.orig_pixmap.rect.height) * 0.5;

    this.fov_radius = pixmap_size * 5;
    this.size = pixmap_size;

    this.sex = Math.random() > 0.5 ? Female : Male;

    this.randomize_step = 0;
    this.food_target = undefined;
    this.courtshipping = undefined;

    this.separation = new Point(0, 0);
    this.cohesion = new Point(0, 0);
    this.alignment = new Point(0, 0);

    this.paint_entity = this.paint;

    this.paint = function(painter) {
        this.paint_entity(painter);

        if(!ShowInfo) return;

        r = this.fov_radius;

        if(this.visible > 0)
            painter.pen = red_pen;
        painter.drawEllipse(-r, -r, r*2, r*2);
        painter.pen = red_pen;
        painter.drawLine(0, 0, this.separation.x * r, this.separation.y * r);
        painter.pen = blue_pen;
        painter.drawLine(0, 0, this.cohesion.x * r, this.cohesion.y * r);
        painter.pen = green_pen;
        painter.drawLine(0, 0, this.alignment.x * r, this.alignment.y * r);
        painter.pen = white_pen;
        painter.drawLine(0, 0, this.direction.x * r, this.direction.y * r);
    }

    this.perceives = function(other, dist) {
        if(dist > this.fov_radius) return false;

        var fov_angle = angle_between(
                -this.direction.x, -this.direction.y,
                other.pos.x - this.pos.x, other.pos.y - this.pos.y);

        return fov_angle > 0.4;
    }

    this.think = function(timestep, neighbors) {
        var separation = new Point(0, 0);
        var cohesion = new Point(0, 0);
        var alignment = new Point(0, 0);

        var visible = 0;
        var other_courtshipping = undefined;
        var food_target_dist = undefined;

        for(var i=0, info; info=neighbors[i]; i++) {
            var other = info[0], dist = info[1];

            switch(other.type) {
                case BoidType:
                    if(other.courtshipping == this) {
                        other_courtshipping = this;
                    } else if(this.next_breed == 0 && this.energy > 0) {
                        if(
                                this.courtshipping == undefined &&
                                other.sex != this.sex) {
                            this.courtshipping = other;
                        }
                    }

                    // Flocking behaviour ignores fishes of a different species.
                    if(Math.floor(this.value) != Math.floor(other.value)) {
                        continue;
                    }
                    visible++;

                    // Separation
                    if(dist < 0.01) {
                        separation.x += Math.random();
                        separation.y += Math.random();
                    } else {
                        separation.add(
                                delta(other.pos, this.pos).scale(
                                        1 / dist - 1 / this.fov_radius));
                    }

                    // Cohesion
                    cohesion.add(
                            delta(this.pos, other.pos).scale(
                                    1 / this.fov_radius));

                    // Alignment
                    alignment.add(other.direction);
                break;
                case FoodType:
                    if(
                            this.food_target == undefined || 
                            food_target_dist > dist) {
                        this.food_target = other;
                        food_target_dist = dist;
                    }
                break;
            }
        }

        var direction = new Point(0, 0);

        // Direction from flocking behaviour.
        if(visible > 0) {
            direction.add(new Point(
                    (separation.x + cohesion.x + alignment.x) / (3 * visible),
                    (separation.y + cohesion.y + alignment.y) / (3 * visible)));
        } else {
            direction.add(this.direction);
        }

        if(this.randomize_step > 0) {
            this.randomize_step--;
        } else {
            this.randomize_step = 10 + Math.floor(Math.random() * 10);
            var explore_dir = new Point(
                    (0.5 - Math.random()) * 2, (0.5 - Math.random()) * 2);
            direction.scale(0.2).add(explore_dir.scale(0.8));

            this.acceleration += (0.5 - Math.random()) * 0.5;
        }

        if(this.food_target != undefined) {
            var food_dir = delta(this.pos, this.food_target.pos);
            direction.scale(0.4).add(food_dir.scale(0.6));
            this.acceleration = 1;

            // Eat.
            if(food_dir.len() < this.size) {
                amount = this.food_target.eat();
                this.food_target = undefined;
                this.energy += amount;
            } else if(!this.food_target.alive()) {
                this.food_target = undefined;
            }
        }

        if(other_courtshipping != undefined) {
            var flee_dir = delta(this.pos, other_courtshipping.pos).scale(-1);
            direction.scale(0.1).add(flee_dir.scale(0.9));
            this.acceleration = 1;
        }

        if(this.courtshipping != undefined) {
            var chase_dir = delta(this.pos, this.courtshipping.pos);
            direction.scale(0.1).add(chase_dir.scale(0.9));
            this.acceleration = 1;
            if(this.energy <= 0) {
                this.courtshipping = undefined;
            } else if(chase_dir.len() < this.size) {
                this.next_breed += this.breed_time;
                // Only add new boids if the upper limit is not reached.
                if(world.entities.length < world.max_entities) {
                    world.add_entity(create_fish(
                            this.pos.x, this.pos.y,
                            this.value + this.courtshipping.value));
                }
                this.courtshipping = undefined;
            }
        }

        // Force boids back to the center of the fishbowl if they are to close
        // to the edge.
        var dist_center = this.pos.len();
        var rel_dist_center = dist_center / (plasmoid.rect.width * 0.5);

        if(rel_dist_center > 0.9) {
            var f = (rel_dist_center - 0.9) * 10;
            var center_dir = scale(this.pos, -1 / dist_center);
            direction.scale(1 - f).add(center_dir.scale(f));
        }

        // Acceleration is decreasing over time.
        this.acceleration *= 0.9;

        this.speed = 0.5 * this.speed +
            this.average_speed * (1 + this.acceleration * 0.5) * 0.5;
        this.energy = Math.max(0, this.energy - this.speed * timestep);
        if(this.energy == 0)
            this.speed = Math.min(this.average_speed, this.speed);

        // Normalize direction.
        direction.normalize();

        // y doesn't sum up to one which will let the boids tend to swim
        // horizontally.
        this.direction.x = 0.75 * this.direction.x + 0.25 * direction.x;
        this.direction.y = 0.75 * this.direction.y + 0.225 * direction.y;

        this.age += timestep;
        if(Math.ceil((this.age / this.max_age) * AgeStages) > this.age_stage) {
            this.age_stage++;
            this.size = MinBoidSize +
                (1 - MinBoidSize) * this.age_stage / AgeStages;
            this.resize();
        }

        this.next_breed = Math.max(0, this.next_breed - timestep);

        // Store values just in case they should be visualized.
        this.separation = separation;
        this.cohesion = cohesion;
        this.alignment = alignment;
    }

    this.str = function() {
        return "(" + this.pos.str() + ")";
    }

    this.alive = function() {
        return this.age < this.max_age;
    }
}

World = function() {
    // Container for all entities.
    this.entities = [];
    this.new_entities = [];
    this.distances = [];

    this.features = [];

    this.max_entities = undefined;
    this.sim_timestep = undefined;
    this.update_timestep = undefined;

    this.get_distance = function(a, b) {
        // Returns the distance from entity with index a to the entity with
        // index b.
        if(a > b) {
            var t = a;
            a = b;
            b = t;
        }

        index = (a * (this.entities.length - 1) -
                Math.floor((a - 1) * a * 0.5) + b - a - 1);

        return this.distances[index];
    }

    this.step = function() {
        // Collect dead entities.
        var dead = [];

        for(var i=0, entity; entity=this.entities[i]; i++) {
            if(entity.alive()) continue;

            dead.push(i);
        }

        dead.reverse();
        // Strange, this doesn't work with the above iteration style.
        for(var i=0; i<dead.length; i++) {
            this.entities.splice(dead[i], 1);
        }

        // Add new entities.
        for(var i=0,entity; entity=this.new_entities[i]; i++) {
            this.entities.push(entity);
        }
        this.new_entities = [];

        // Update distances between entities.
        this.distances = [];
        for(var a=0, boid_a; boid_a=this.entities[a]; a++) {
            for(var b=a+1, boid_b; boid_b=this.entities[b]; b++) {
                // Calculate distance between boid a and b.
                this.distances.push(delta(boid_a.pos, boid_b.pos).len());
           }
        }

        for(var i=0, entity; entity=this.entities[i]; i++) {
            // Ignore entities which can't think.
            if(entity.think == undefined) continue;

            var neighbors = [];

            for(var j=0, other; other=this.entities[j]; j++) {
                if(other == entity) continue;
                dist = this.get_distance(i, j);
                if(!entity.perceives(other, dist)) continue;

                neighbors.push([other, dist]);
            }

            entity.think(this.sim_timestep, neighbors);
        }
    }

    this.move = function() {
        for(var i=0, entity; entity=this.entities[i]; i++) {
            entity.pos.add(scale(
                    entity.direction, entity.speed * this.update_timestep));
        }
    }

    this.draw = function(painter) {
        var r = plasmoid.rect, y = r.y + r.height;

        // Draw features.
        for(var i = 0,f; f=this.features[i]; i++) {
            painter.drawPixmap(
                    r.x + (r.width - f[1].rect.width) * f[0],
                    y - f[1].rect.height, f[1]);
        }

        // Draw entities.
        painter.translate(r.x + r.width / 2, r.y + r.height / 2);
        for(var i = 0, e; e = this.entities[i]; i++) {
            painter.save();
            painter.translate(e.pos.x, e.pos.y);
            e.paint(painter);
            painter.restore();
        }
    }

    this.add_entity = function(entity) {
        this.new_entities.push(entity);
    }

    this.count_fishes = function() {
        var count = 0;
        for(var i = 0, e; e = this.entities[i]; i++) {
            if(e.think != undefined) {
                count++;
            }
        }
        return count;
    }

    this.rebuild_features = function(feature_count) {
        // Calculate sum of weights.
        var sum_weights = 0;
        for(var i = 0,f; f=Features[i]; i++) {
            sum_weights += f[0];
        }

        // Rebuild features.
        this.features = [];
        var vary_x = (1 / feature_count) * 0.5;
        while(this.features.length < feature_count) {
            // Select a feature index i.
            var i, r = uniform(0, sum_weights), current = 0;
            for(i = 0; i < Features.length; i++) {
                current += Features[i][0];
                if(r <= current) break;
            }

            var pos_x = this.features.length / feature_count + 
                    vary_x * Math.random();

            this.features.push([pos_x, new Svg(Features[i][1]).pixmap()]);
        }
    }
}

// Finally create the world.
var world;

initialize = function() {
    world = new World();

    var step = function() {
        // Steps through the world.
        world.step();
        sim_timer.start();
    }

    var update = function() {
        world.move();
        plasmoid.update();
        update_timer.start();
    }

    // The simulation heartbeat timer.
    var sim_timer = new QTimer();
    sim_timer.timeout.connect(step);
    sim_timer.singleShot = true;

    // The update heartbeat timer.
    var update_timer = new QTimer();
    update_timer.timeout.connect(update);
    update_timer.singleShot = true;

    // Create a timer for bubbles.
    var create_bubble = function() {
        if(world.entities.length < world.max_entities) {
            var width = plasmoid.rect.width * 0.4;

            world.add_entity(new Bubble(
                    uniform(-width, width), plasmoid.rect.height * 0.4));
        }

        bubble_timer.start((1 + Math.random()) * BubbleTime);
    }

    var bubble_timer = new QTimer();
    bubble_timer.singleShot = true;
    bubble_timer.timeout.connect(create_bubble);

    // Create a timer for auto-feeding.
    var autofeed = function() {
        feed();
        autofeed_timer.start(uniform(MinAutofeedTime, MaxAutofeedTime));
    }

    var autofeed_timer = new QTimer();
    autofeed_timer.singleShot = true;
    autofeed_timer.timeout.connect(autofeed);

    // Create a timer for auto-buying.
    var autobuy = function() {
        if(world.count_fishes() < AutoBuyLimit) {
            world.add_entity(create_default_fish());
        }
        autobuy_timer.start(AutobuyTime);
    }

    var autobuy_timer = new QTimer();
    autobuy_timer.singleShot = true;
    autobuy_timer.timeout.connect(autobuy);

    // Timer functions.
    var running = true, autofeeding = true, autobuying = true;
    var enable_timer = function(timer, enable) {
        // Convenience function to enable a timer.
        if(enable) { timer.start(); } else { timer.stop(); }
    }

    var toggle_timers = function() {
        enable_timer(update_timer, running);
        enable_timer(sim_timer, running);
        enable_timer(bubble_timer, running);
        enable_timer(autofeed_timer, running && autofeeding);
        enable_timer(autobuy_timer, running && autobuying);
    }

    // Create a button for feeding fishes.
    var feed_button = new IconWidget();
    feed_button.icon = new QIcon(Svg("food").pixmap());

    var feed = function() {
        if(world.entities.length >= world.max_entities) return;

        var max_x = plasmoid.rect.width * 0.4;

        world.add_entity(new Food(
                uniform(-max_x, max_x), -plasmoid.rect.height * 0.4));
    }

    feed_button.clicked.connect(feed);

    // Create a button for buying a new fish.
    var buy_fish_button = new IconWidget();
    buy_fish_button.icon = new QIcon(Svg("fish1").pixmap());
    buy_fish_button.x += 20;

    var buy_fish = function() {
        if(world.entities.length >= world.max_entities) return;

        var max_x = plasmoid.rect.width * 0.4;
        var max_y = plasmoid.rect.height * 0.4;

        world.add_entity(
            create_fish(uniform(-max_x, max_x), uniform(-max_y, max_y), 0));
    }

    buy_fish_button.clicked.connect(buy_fish);

    // Create a button for suspending the simulation.
    var sleep_button = new IconWidget();
    sleep_button.icon = new QIcon(Svg("sleep").pixmap());
    sleep_button.x += 40;

    var toggle_running = function() {
        running = !running;
        toggle_timers();
    }

    sleep_button.clicked.connect(toggle_running);

    // Setup actions.
    plasmoid.action_toggle_autofeed = function() {
        autofeeding = !autofeeding;
        toggle_timers();
    }
    plasmoid.setAction("toggle_autofeed", "Toggle Auto-Feed");

    plasmoid.action_toggle_autobuy = function() {
        autobuying = !autobuying;
        toggle_timers();
    }
    plasmoid.setAction("toggle_autobuy", "Toggle Auto-Buy");

    // Setup plasmoid callbacks.
    plasmoid.paintInterface = function(painter) {
        world.draw(painter);
    }

    plasmoid.configChanged = function() {
        // Reloads the configuration.
        world.sim_timestep = 1 / plasmoid.readConfig("sps")
        sim_timer.interval = world.sim_timestep * 1000;
        world.update_timestep = 1 / plasmoid.readConfig("fps");
        update_timer.interval = world.update_timestep * 1000;

        // TODO excess entities are not removed.
        world.max_entities = plasmoid.readConfig("entities");

        world.rebuild_features(plasmoid.readConfig("features"));
    }

    // Initiate configuration.
    plasmoid.configChanged();

    // Add initial fishes.
    for(var i = 0; i < AutoBuyLimit; i++) {
        world.add_entity(create_default_fish());
    }

    // Start heartbeat timers.
    toggle_timers();
}

initialize();
