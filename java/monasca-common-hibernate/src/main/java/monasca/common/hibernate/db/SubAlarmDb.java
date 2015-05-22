/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.annotations.Type;
import org.joda.time.DateTime;

@Entity
@Table(name = "sub_alarm")
public class SubAlarmDb extends CreateUpdateDate{

  @Id
  @Column(name = "id", length = 36)
  private String id;

  @Column(name = "alarm_id", length = 36, nullable = false)
  private String alarm_id;

  @Column(name = "sub_expression_id", length = 36)
  private String sub_expression_id;

  @Column(name = "expression", nullable = false)
  @Type(type = "text")
  private String expression = "";

  public SubAlarmDb() {
    super();
  }

  public SubAlarmDb(String id, String alarm_id, String sub_expression_id, String expression, DateTime created_at, DateTime updated_at) {
    super(created_at, updated_at);
    this.id = id;
    this.alarm_id = alarm_id;
    this.sub_expression_id = sub_expression_id;
    this.expression = expression;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getAlarm_id() {
    return alarm_id;
  }

  public void setAlarm_id(String alarm_id) {
    this.alarm_id = alarm_id;
  }

  public String getExpression() {
    return expression;
  }

  public void setExpression(String expression) {
    this.expression = expression;
  }

  public String getSub_expression_id() {
    return sub_expression_id;
  }

  public void setSub_expression_id(String sub_expression_id) {
    this.sub_expression_id = sub_expression_id;
  }
}
