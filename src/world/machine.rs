use bevy::prelude::*;

#[derive(Component)]
pub struct Machine {
    variant: MachineType,
}
impl Machine {
    pub fn spawn(mut commands: Commands) {
        commands.spawn((
            SpriteBundle {
                sprite: Sprite {
                    ..default()
                },
                ..default()
            },
            Self {
                variant: MachineType { name: "Default machine" },
            }
        ));
    }
}

pub struct MachineType {
    name: &'static str
}