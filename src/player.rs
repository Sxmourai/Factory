use bevy::prelude::*;

#[derive(Component)]
pub struct Player {
    pub speed: f32,
    pub pos: Vec2
}

pub fn player_movement(
    mut characters: Query<(&mut Transform, &Player)>,
    input: Res<Input<KeyCode>>,
    time: Res<Time>,
) {
    for (mut transform, player) in &mut characters {
        let movement_speed = player.speed * time.delta_seconds();
        if input.pressed(KeyCode::Z) {
            transform.translation.y += movement_speed;
        }
        if input.pressed(KeyCode::S) {
            transform.translation.y -= movement_speed;
        }
        if input.pressed(KeyCode::D) {
            transform.translation.x += movement_speed;
        }
        if input.pressed(KeyCode::Q) {
            transform.translation.x -= movement_speed;
        }
    }
}