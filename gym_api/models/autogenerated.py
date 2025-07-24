from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Exercise(Base):
    __tablename__ = 'exercise'
    __table_args__ = (
        PrimaryKeyConstraint('exercise_id', name='exercise_pkey'),
        {'schema': 'gym'}
    )

    exercise_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)

    card: Mapped[List['Card']] = relationship('Card', back_populates='exercise')


class ExerciseDesc(Base):
    __tablename__ = 'exercise_desc'
    __table_args__ = (
        PrimaryKeyConstraint('exercise_desc_id', name='exercise_desc_pkey'),
        {'schema': 'gym'}
    )

    exercise_desc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)

    card: Mapped[List['Card']] = relationship('Card', back_populates='exercise_desc')


class Link(Base):
    __tablename__ = 'link'
    __table_args__ = (
        PrimaryKeyConstraint('link_id', name='link_pkey'),
        {'schema': 'gym'}
    )

    link_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(Text)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    title: Mapped[Optional[str]] = mapped_column(Text)
    close_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='user_pkey'),
        UniqueConstraint('email', name='user_email_key'),
        UniqueConstraint('phone', name='user_phone_key'),
        UniqueConstraint('telegram_id', name='user_telegram_id_key'),
        {'schema': 'gym'}
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[str] = mapped_column(Text)
    username: Mapped[Optional[str]] = mapped_column(Text)
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    photo: Mapped[Optional[str]] = mapped_column(Text)

    gymer: Mapped[List['Gymer']] = relationship('Gymer', back_populates='user')
    master: Mapped[List['Master']] = relationship('Master', back_populates='user')


class Gymer(Base):
    __tablename__ = 'gymer'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['gym.user.user_id'], name='gymer_user_id_fkey'),
        PrimaryKeyConstraint('gymer_id', name='gymer_pkey'),
        {'schema': 'gym'}
    )

    gymer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user: Mapped[Optional['User']] = relationship('User', back_populates='gymer')
    task_group: Mapped[List['TaskGroup']] = relationship('TaskGroup', back_populates='gymer')


class Master(Base):
    __tablename__ = 'master'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['gym.user.user_id'], name='master_user_id_fkey'),
        PrimaryKeyConstraint('master_id', name='master_pkey'),
        {'schema': 'gym'}
    )

    master_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user: Mapped[Optional['User']] = relationship('User', back_populates='master')
    card: Mapped[List['Card']] = relationship('Card', back_populates='master')
    task_group: Mapped[List['TaskGroup']] = relationship('TaskGroup', back_populates='master')


class Card(Base):
    __tablename__ = 'card'
    __table_args__ = (
        ForeignKeyConstraint(['exercise_desc_id'], ['gym.exercise_desc.exercise_desc_id'], name='card_exercise_desc_id_fkey'),
        ForeignKeyConstraint(['exercise_id'], ['gym.exercise.exercise_id'], name='card_exercise_id_fkey'),
        ForeignKeyConstraint(['master_id'], ['gym.master.master_id'], name='card_master_id_fkey'),
        PrimaryKeyConstraint('card_id', name='card_pkey'),
        {'schema': 'gym'}
    )

    card_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    status: Mapped[str] = mapped_column(String(15), server_default=text("'active'::character varying"))
    master_id: Mapped[Optional[int]] = mapped_column(Integer)
    exercise_id: Mapped[Optional[int]] = mapped_column(Integer)
    exercise_desc_id: Mapped[Optional[int]] = mapped_column(Integer)
    update_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    title: Mapped[Optional[str]] = mapped_column(String(45))

    exercise_desc: Mapped[Optional['ExerciseDesc']] = relationship('ExerciseDesc', back_populates='card')
    exercise: Mapped[Optional['Exercise']] = relationship('Exercise', back_populates='card')
    master: Mapped[Optional['Master']] = relationship('Master', back_populates='card')
    task: Mapped[List['Task']] = relationship('Task', back_populates='card')


class MasterGym(Base):
    __tablename__= 'master_gym'
    __table_args__ = (
        PrimaryKeyConstraint('master_id', 'gymer_id', 'create_dttm'),
        ForeignKeyConstraint(['gymer_id'], ['gym.gymer.gymer_id'], name='master_gym_gymer_id_fkey'),
        ForeignKeyConstraint(['master_id'], ['gym.master.master_id'], name='master_gym_master_id_fkey'),    
        {'schema': 'gym'}
    )
    master_id: Mapped[int] = mapped_column(Integer)
    gymer_id: Mapped[Optional[int]] = mapped_column(Integer)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    close_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))


class TaskGroup(Base):
    __tablename__ = 'task_group'
    __table_args__ = (
        ForeignKeyConstraint(['gymer_id'], ['gym.gymer.gymer_id'], name='task_group_gymer_id_fkey'),
        ForeignKeyConstraint(['master_id'], ['gym.master.master_id'], name='task_group_master_id_fkey'),
        PrimaryKeyConstraint('task_group_id', name='task_group_pkey'),
        {'schema': 'gym'}
    )

    task_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(15), server_default=text("'planed'::character varying"))
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    master_id: Mapped[Optional[int]] = mapped_column(Integer)
    gymer_id: Mapped[Optional[int]] = mapped_column(Integer)
    update_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    start_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    order_idx: Mapped[Optional[int]] = mapped_column(Integer)

    gymer: Mapped[Optional['Gymer']] = relationship('Gymer', back_populates='task_group')
    master: Mapped[Optional['Master']] = relationship('Master', back_populates='task_group')
    task: Mapped[List['Task']] = relationship('Task', back_populates='task_group')

class LinkCard(Base):
    __tablename__ = 'link_card'
    __table_args__ = (
        ForeignKeyConstraint(['card_id'], ['gym.card.card_id'], name='link_card_card_id_fkey'),
        ForeignKeyConstraint(['link_id'], ['gym.link.link_id'], name='link_card_link_id_fkey'),
        {'schema': 'gym'}
    )

    link_id: Mapped[int] = mapped_column(Integer)
    card_id: Mapped[int] = mapped_column(Integer)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    close_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = (
        ForeignKeyConstraint(['card_id'], ['gym.card.card_id'], name='task_card_id_fkey'),
        ForeignKeyConstraint(['task_group_id'], ['gym.task_group.task_group_id'], name='task_task_group_id_fkey'),
        PrimaryKeyConstraint('task_id', name='task_pkey'),
        {'schema': 'gym'}
    )

    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(15), server_default=text("'planed'::character varying"))
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    task_group_id: Mapped[Optional[int]] = mapped_column(Integer)
    card_id: Mapped[Optional[int]] = mapped_column(Integer)
    update_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    order_idx: Mapped[Optional[int]] = mapped_column(Integer)

    card: Mapped[Optional['Card']] = relationship('Card', back_populates='task')
    task_group: Mapped[Optional['TaskGroup']] = relationship('TaskGroup', back_populates='task')
    task_properties: Mapped[List['TaskProperties']] = relationship('TaskProperties', back_populates='task')


class TaskProperties(Base):
    __tablename__ = 'task_properties'
    __table_args__ = (
        ForeignKeyConstraint(['task_id'], ['gym.task.task_id'], name='task_properties_task_id_fkey'),
        PrimaryKeyConstraint('task_properties_id', name='task_properties_pkey'),
        {'schema': 'gym'}
    )

    task_properties_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_id: Mapped[Optional[int]] = mapped_column(Integer)
    max_weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 1))
    min_weight: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 1))
    rest: Mapped[Optional[int]] = mapped_column(Integer)

    task: Mapped[Optional['Task']] = relationship('Task', back_populates='task_properties')
    set: Mapped[List['Set']] = relationship('Set', back_populates='task_properties')


class Set(Base):
    __tablename__ = 'set'
    __table_args__ = (
        ForeignKeyConstraint(['task_properties_id'], ['gym.task_properties.task_properties_id'], name='set_task_properties_id_fkey'),
        PrimaryKeyConstraint('set_id', name='set_pkey'),
        {'schema': 'gym'}
    )

    set_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_properties_id: Mapped[Optional[int]] = mapped_column(Integer)
    fact_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 1))
    fact_rep: Mapped[Optional[int]] = mapped_column(Integer)
    plan_value: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 1))
    plan_rep: Mapped[Optional[int]] = mapped_column(Integer)

    task_properties: Mapped[Optional['TaskProperties']] = relationship('TaskProperties', back_populates='set')
