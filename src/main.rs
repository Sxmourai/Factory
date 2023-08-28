mod setup;
mod renderer;
mod player;
mod ui;

use bevy::prelude::*;
use setup::SetupPlugin;

fn main() {
    App::new()
    .add_plugins(SetupPlugin)
    .run();
}