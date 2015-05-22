/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.hibernate.db;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.Id;
import javax.persistence.Table;

import monasca.common.model.alarm.AlarmState;
import org.joda.time.DateTime;

@Entity
@Table(name = "alarm")
public class AlarmDb extends CreateUpdateDate{

  @Id
  @Column(name = "id", length = 36)
  private String id;

  @Column(name = "alarm_definition_id", length = 36)
  private String alarm_definition_id;

  @Column(name = "state")
  @Enumerated(EnumType.STRING)
  private AlarmState state;

  public AlarmDb() {
    super();
  }

  public AlarmDb(String id, String alarm_definition_id, AlarmState state, DateTime created_at, DateTime updated_at) {
    super(created_at, updated_at);
    this.id = id;
    this.alarm_definition_id = alarm_definition_id;
    this.state = state;

  }

  public String getAlarm_definition_id() {
    return alarm_definition_id;
  }

  public void setAlarm_definition_id(String alarm_definition_id) {
    this.alarm_definition_id = alarm_definition_id;
  }

  public AlarmState getState() {
    return state;
  }

  public void setState(AlarmState state) {
    this.state = state;
  }
}
